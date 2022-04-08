import pandas as pd
import numpy as np
import os
import json
import matplotlib

matplotlib.use("TKAgg")
import json
from application import jsonify, Response
from collections import OrderedDict, defaultdict


def getDistributionData(df):

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

    # df['ID'] = df['ID'].astype('category')

    # 1-2 dtype에 따라서 df를 numeric과 categroical로 나눔
    df_numeric = df.select_dtypes(exclude=["category", "datetime64"]).copy()

    """ 2) Numeric 정보를 담고 있는 변수 생성 과정 """
    """2-1 Numeric"""
    # 2-1-1) 각 numeric 관련 변수 생성

    """ Distribution  & Interval """
    distribution_features = OrderedDict()
    # interval_features = OrderedDict()
    distribution_features_column = []

    for each in df_numeric.columns:
        # pd.to_numeric()로 형 변환을 안해주면 오류남 (TypeError: '<=' not supported between instances of 'float' and 'str')
        if df_numeric[each].dtypes == float:
            dictdata = {
                "min": float(np.round(df_numeric[each].min(), 2)),
                "max": float(np.round(df_numeric[each].max(), 2)),
            }
        else:
            dictdata = {
                "min": int(df_numeric[each].min()),
                "max": int(df_numeric[each].max()),
            }
        # interval_features[each] = dictdata
        distribution_features[each] = df_numeric[each].value_counts(bins=20).to_list()

        #   배열 초기화
        dictdata = {}
        distribution_features_column = []

    return json.dumps(distribution_features)
