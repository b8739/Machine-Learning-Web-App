# from app import df
import pandas as pd 
import numpy as np 
import os
import json
import matplotlib
import json
from app import jsonify, Response
from collections import OrderedDict, defaultdict

def summarizeData(df):
  
  ''' 1) 데이터 타입 전처리 (object -> numeric/category)'''
  # 1-1 object로 분류된 category 데이터의 dtype을 'category'로 변경 
  category_features = []
  threshold = 10
 
  for each in df.columns:
    if df[each].nunique() < threshold:
        category_features.append(each)
    elif each == 'ts':
        category_features.append(each)

  for each in category_features:
    df[each] = df[each].astype('category')
    
  df['ID'] = df['ID'].astype('category')

  # 1-2 dtype에 따라서 df를 numeric과 categroical로 나눔
  df_numeric = df.select_dtypes(exclude = ['category']).copy()
  df_categorical = df.select_dtypes(include = ['category'] ).copy()
  del df_categorical['ID']
  # 1-3 csv 파일이 크면 float이나 int도 object로 읽어지는 문제가 있음. 이에 따라 수동으로 데이터타입을 변경 (object -> unsigned numeric)
  for each in df_numeric:
    df[each] = pd.to_numeric(df[each], downcast="unsigned")
  
  ''' 2) Numeric 정보를 담고 있는 변수 생성 과정 '''
  '''2-1 Numeric'''
  # 2-1-1) 각 numeric 관련 변수 생성
  df_numeric_columns = list((df_numeric).columns)

  df_numeric_mean =  df_numeric.mean().round(1)
  df_numeric_median =  df_numeric.median().round(1)
  df_numeric_std = df_numeric.std().round(1)
  df_numeric_Q1 = df_numeric.quantile(.25).round(2)
  df_numeric_Q2 = df_numeric.quantile(.5).round(2)
  df_numeric_Q3 = df_numeric.quantile(.75).round(2)
  df_numeric_Q4 = df_numeric.quantile(1).round(2)
  df_numeric_numOfNA = df_numeric.isnull().sum()

  # 2-1-2 모든 numeric 변수들을 담고 있는 종합 Info 변수 생성
  df_numeric_info = pd.DataFrame(index=list(df_numeric.columns)) 
  # 2-1-3 Info 변수에 각 변수 투입

  df_numeric_info.insert(0,'mean',df_numeric_mean)
  df_numeric_info.insert(1,'median',df_numeric_median)
  df_numeric_info.insert(2,'standard deviation',df_numeric_std)
  df_numeric_info.insert(3,'Q1',df_numeric_Q1)
  df_numeric_info.insert(4,'Q2',df_numeric_Q2)
  df_numeric_info.insert(5,'Q3',df_numeric_Q3)
  df_numeric_info.insert(6,'Q4',df_numeric_Q4)
  df_numeric_info.insert(7,'numOfNA',df_numeric_numOfNA)
  # distribution 데이터 (frequency) 
  distribution_features =  OrderedDict()
  interval_features =  OrderedDict()
  distribution_features_column = []

  for each in df_numeric.columns:
    dictdata = {'min':float(df_numeric[each].min()),'max':float(df_numeric[each].max())}

    interval_features[each]=dictdata
    distribution_features[each]=df_numeric[each].value_counts(bins=20).to_list()
  
  #   배열 초기화
    dictdata = {}
    distribution_features_column = []

  
  #####################################################
  '''2-2 Category'''
  # 2-2-1) 각 category 관련 변수 생성
  df_categorical_columns = list((df_categorical).columns)
  # df_categorical_mostCommon = df_categorical.value_counts().idxmax()//argmax오류나서 일단 주석처리
  series_categorical_numOfNa = df_categorical.isnull().sum()

  sampleForClass= {}
  for value in df_categorical_columns:
    sampleForClass[value] = (df_categorical[value].value_counts(normalize=True) * 100).round(2).to_dict()
  # print(sampleForClass)
  df_categorical_etc = df_categorical.agg(['size', 'nunique'])

  # 2-2-2) 모든 category 변수들을 담고 있는 종합 Info 변수 생성
  df_categorical_info = pd.DataFrame(index=list(df_categorical.columns)) 


  # 2-2-3) Info 변수에 각 변수 투입
  # df_categorical_info.insert(0,'mostCommon',df_categorical_mostCommon) //argmax오류나서 일단 주석처리
  df_categorical_info.insert(0,'numOfNA',series_categorical_numOfNa) # index 일단 0로 변경, 나중에 다시 1으로

  df_categorical_etc_index = list(df_categorical_etc.index)

  for index,value in enumerate(df_categorical_etc_index):
    df_categorical_info.insert(index,value,df_categorical_etc.iloc[index])
  # df에서 ID의 mostCommon값을 수동으로 str로 변환해주어야, 'int 64 json not serializable' 메시지가 안뜸

  # df_categorical_info = df_categorical_info.astype({'mostCommon': 'str'})
  ''' type identify '''
  typelist = []
  typetype = {}
  del df['ID']
  for index,value in enumerate(df.columns):
    if df[value].nunique() < threshold:
      valueType = 'category'
    else:
      valueType = 'numeric'
    # typetype[value] = valueType
    typelist.append({'name':value,'type':valueType})

  df_typetype = pd.DataFrame(typelist)
  df_typetype = df_typetype.set_index('name')


  ''' 3) Return '''

# 반환
  summarizedInfo = {'numeric':df_numeric_info.to_dict(), 'category':df_categorical_info.to_dict()}
  summarizedColumns = {'numeric':df_numeric_columns,'category':df_categorical_columns}
  
  finalSummary = OrderedDict()
  
  finalSummary = {'datatype':df_typetype.to_dict(orient='list',into=OrderedDict),'categorical':df_categorical_info.to_dict(orient='index',into=OrderedDict),'numeric':df_numeric_info.to_dict(orient='index'),'distribution':distribution_features,'interval':interval_features,'sampleForClass':sampleForClass}
  print(finalSummary)
  # return  finalSummary
  return json.dumps(finalSummary)
  
  # return jsonify(finalSummary) 