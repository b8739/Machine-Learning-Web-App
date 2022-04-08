import pandas as pd
import numpy as np
import os
import json
import matplotlib

matplotlib.use("TKAgg")
import json

from application import jsonify, Response


from collections import OrderedDict, defaultdict


def summarizeData(df):

    """1) 데이터 타입 전처리 (object -> numeric/category)"""
    # 1-1 object로 분류된 category 데이터의 dtype을 'category'로 변경
    category_features = []
    numericfeatures = []
    timeSeries = None
    threshold = 5

    dataType = {}

    """ type identify """
    if "ID" in df:
        del df["ID"]

    for each in df.columns:
        if df[each].nunique() < threshold:
            category_features.append(each)
            valueType = "category"

        elif (
            each == "ts"
            or each == "Date"
            or each == "Dates"
            or each == "dates"
            or each == "time"
            or each == "timeseries"
        ):
            df[each] = pd.to_datetime(df[each])  # date type 으로 변경
            valueType = "date"
            # parse_dates=['date'] 읽을때 쓸수 있는 방법. 고려해보기
            # np.issubdtype(df[each].dtype, np.datetime64)
        elif df[each].dtypes == float or df[each].dtypes == int:
            numericfeatures.append(each)
            valueType = str(df[each].dtypes)
        else:
            category_features.append(each)
            valueType = str(df[each].dtypes)
        dataType[each] = valueType

    """ object -> category """
    for each in category_features:
        df[each] = df[each].astype("category")

    # df['ID'] = df['ID'].astype('category')

    # 1-2 dtype에 따라서 df를 numeric과 categroical로 나눔
    df_numeric = df.select_dtypes(exclude=["category", "datetime64"]).copy()
    df_timeSeries = df.select_dtypes(exclude=["datetime64"]).copy()
    df_categorical = df.select_dtypes(include=["category"]).copy()

    # 혹시나 datetime이 category로 되어서 key로 timestamp안된다고 할까봐 넣은건데 이렇면 sample for class \n이렇게 나옴
    # for each in df_categorical:
    #   df_categorical[each] = str(df_categorical[each])

    # del df_categorical['ID']
    # 1-3 csv 파일이 크면 float이나 int도 object로 읽어지는 문제가 있음. 이에 따라 수동으로 데이터타입을 변경 (object -> unsigned numeric)
    # for each in df_numeric:
    #   df[each] = pd.to_numeric(df[each], downcast="unsigned")

    """ 2) Numeric 정보를 담고 있는 변수 생성 과정 """
    """2-1 Numeric"""
    # 2-1-1) 각 numeric 관련 변수 생성
    df_numeric_columns = list((df_numeric).columns)
    df_dtypes = df_numeric.dtypes
    for index, value in df_dtypes.items():
        df_dtypes[index] = str(value)
    df_numeric_min = np.round(df_numeric.min(), 2)
    df_numeric_max = np.round(df_numeric.max(), 2)
    df_numeric_mean = np.round(df_numeric.mean(), 2)
    df_numeric_mode = np.round(df_numeric, 3).mode().loc[0]

    df_numeric_median = np.round(df_numeric.median(), 1)
    df_numeric_std = np.round(df_numeric.std(), 1)
    df_numeric_Q1 = np.round(df_numeric.quantile(0.25), 2)
    df_numeric_Q2 = np.round(df_numeric.quantile(0.5), 2)
    df_numeric_Q3 = np.round(df_numeric.quantile(0.75), 2)
    df_numeric_Q4 = np.round(df_numeric.quantile(1), 2)
    df_numeric_numOfNA = df_numeric.isnull().sum()

    # 2-1-2 모든 numeric 변수들을 담고 있는 종합 Info 변수 생성
    # 2-1-3 Info 변수에 각 변수 투입

    d = {
        "name": df_numeric_columns,
        "dtype": df_dtypes,
        "min": df_numeric_min,
        "max": df_numeric_max,
        "mean": df_numeric_mean,
        "mode": df_numeric_mode,
        "median": df_numeric_median,
        "std": df_numeric_std,
        "Q1": df_numeric_Q1,
        "Q2": df_numeric_Q2,
        "Q3": df_numeric_Q3,
        "Q4": df_numeric_Q4,
        "numOfNA": df_numeric_numOfNA,
    }

    df_numeric_info = pd.DataFrame(data=d, index=None)

    """ Distribution  & Interval """
    # distribution_features = OrderedDict()
    # interval_features = OrderedDict()
    # distribution_features_column = []

    # for each in df_numeric.columns:
    #     # pd.to_numeric()로 형 변환을 안해주면 오류남 (TypeError: '<=' not supported between instances of 'float' and 'str')
    #     if df_numeric[each].dtypes == float:
    #         dictdata = {
    #             "min": float(np.round(df_numeric[each].min(), 2)),
    #             "max": float(np.round(df_numeric[each].max(), 2)),
    #         }
    #     else:
    #         dictdata = {
    #             "min": int(df_numeric[each].min()),
    #             "max": int(df_numeric[each].max()),
    #         }
    #     interval_features[each] = dictdata
    #     distribution_features[each] = df_numeric[each].value_counts(bins=20).to_list()

    #     #   배열 초기화
    #     dictdata = {}
    #     distribution_features_column = []

    #####################################################
    """2-2 Category"""
    # 2-2-1) 각 category 관련 변수 생성
    # category가 비어있을 때 빈 dict 만들어서 반환
    sampleForClass = {}

    if category_features == []:
        df_categorical_info = pd.DataFrame()

    else:
        df_categorical_columns = list((df_categorical).columns)
        # df_categorical_mostCommon = df_categorical.value_counts().idxmax()//argmax오류나서 일단 주석처리
        series_categorical_numOfNa = df_categorical.isnull().sum()

        for value in df_categorical_columns:
            sampleForClass[value] = (
                (df_categorical[value].value_counts(normalize=True) * 100)
                .round(2)
                .to_dict()
            )
            if len(sampleForClass[value]) > 10:
                sampleForClass[value] = {}

        # 2-2-2) 모든 category 변수들을 담고 있는 종합 Info 변수 생성
        df_categorical_info = pd.DataFrame(index=list(df_categorical.columns))

        # 2-2-3) Info 변수에 각 변수 투입
        # df_categorical_info.insert(0,'mostCommon',df_categorical_mostCommon) //argmax오류나서 일단 주석처리
        df_categorical_info.insert(
            0, "numOfNA", series_categorical_numOfNa
        )  # index 일단 0로 변경, 나중에 다시 1으로
        df_categorical_info.insert(0, "dtype", "category")
        df_categorical_info.insert(0, "name", df_categorical_columns)

        # agg함수는 괄호안에 있는 size와 nunique를 계산함
        df_categorical_etc = df_categorical.agg(["size", "nunique"])
        df_categorical_etc_index = list(df_categorical_etc.index)

        for index, value in enumerate(df_categorical_etc_index):
            df_categorical_info.insert(index, value, df_categorical_etc.iloc[index])

    """ 3) Return """

    # 반환
    result = pd.concat([df_numeric_info, df_categorical_info])
    result = result.fillna("NA")

    # finalSummary = {
    #     "datatype": dataType,
    #     "categorical": df_categorical_info.to_dict(orient="index", into=OrderedDict),
    #     "numeric": df_numeric_info.to_dict(orient="index"),
    #     "distribution": distribution_features,
    #     "interval": interval_features,
    #     "sampleForClass": sampleForClass,
    # }

    # return json.dumps(finalSummary)
    # print(df_numeric_info)
    # return json.dumps(df_numeric_info.to_dict(orient="records"))  # key가 없이 배열안에 들어가 있는 형태
    return json.dumps(result.to_dict(orient="index"))
