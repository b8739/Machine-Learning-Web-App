import pandas as pd 
import numpy as np 
import os
import datetime
import json
import matplotlib
matplotlib.use("TKAgg")
import json
from application import jsonify, Response
from collections import OrderedDict, defaultdict

def test():

    df = pd.read_csv('/Users/jeongjaeho/attic_project/testcode/boston_house.csv')

    if 'ID' in df:
        del df['ID']
    print (df.dtypes)
    df = df.convert_dtypes() #불분명한 datatype을 하게 바꿔줌
    print (df.dtypes)


    ''' 2) Numeric 정보를 담고 있는 변수 생성 과정 '''
    '''2-1 Numeric'''
    # 2-1-1) 각 numeric 관련 변수 생성
    df_columns = list((df).columns)

    df_mean =  df.mean().round(2)
    df_mode =  df.mode().loc[0]

    df_median =  df.median().round(1)
    df_std = df.std().round(1)
    df_Q1 = df.quantile(.25)
    df_Q2 = df.quantile(.5)
    df_Q3 = df.quantile(.75)
    df_Q4 = df.quantile(1)
    df_numOfNA = df.isnull().sum()

    # 2-1-2 모든 numeric 변수들을 담고 있는 종합 Info 변수 생성
    df_info = pd.DataFrame(index=list(df.columns)) 
    # 2-1-3 Info 변수에 각 변수 투입

    df_info.insert(0,'mean',df_mean)
    df_info.insert(1,'mode',df_mode)
    df_info.insert(2,'median',df_median)
    df_info.insert(3,'standard deviation',df_std)
    df_info.insert(4,'Q1',df_Q1)
    df_info.insert(5,'Q2',df_Q2)
    df_info.insert(6,'Q3',df_Q3)
    df_info.insert(7,'Q4',df_Q4)
    df_info.insert(8,'numOfNA',df_numOfNA)

    # print(df_info)
    # distribution 데이터 (frequency) 
    distribution_features =  OrderedDict()
    interval_features =  OrderedDict()
    distribution_features_column = []

    for each in df.columns:
    # pd.to_numeric()로 형 변환을 안해주면 오류남 (TypeError: '<=' not supported between instances of 'float' and 'str')
        dictdata = {'min':df[each].min(),'max':df[each].max()}
        interval_features[each]=dictdata
        df[each]=pd.to_numeric(df[each])
        distribution_features[each]=df[each].value_counts().to_list()

    #   배열 초기화
    dictdata = {}
    distribution_features_column = []

    ''' 3) Return '''

    # 반환
    finalSummary = OrderedDict()
    df_categorical_info=pd.DataFrame()
    sampleForClass={}
    finalSummary = {'categorical':df_categorical_info.to_dict(orient='index',into=OrderedDict),'numeric':df_info.to_dict(orient='index'),'interval':interval_features,'sampleForClass':sampleForClass}
    print(finalSummary)
    # return  finalSummary
    return json.dumps(finalSummary)

# return jsonify(finalSummary) 