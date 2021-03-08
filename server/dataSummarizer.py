# from app import df
import pandas as pd 
import numpy as np 
import os
import json
import matplotlib
import json
from app import jsonify, Response

def summarizeData(df):
  
  ''' 1) 데이터 타입 전처리 (object -> numeric/category)'''
  # 1-1 object로 분류된 범주형 데이터의 dtype을 'category'로 변경 
  category_features = []
  threshold = 10
 
  for each in df.columns:
    if df[each].nunique() < threshold:
        category_features.append(each)
    elif each == 'Date' :
        category_features.append(each)

  for each in category_features:
    df[each] = df[each].astype('category')

  # 1-2 dtype에 따라서 df를 numeric과 categroical로 나눔
  df_numeric = df.select_dtypes(exclude = ['category']).copy()
  df_categorical = df.select_dtypes(include = ['category'] ).copy()

  # 1-3 csv 파일이 크면 float이나 int도 object로 읽어지는 문제가 있음. 이에 따라 수동으로 데이터타입을 변경 (object -> unsigned numeric)
  for each in df_numeric:
    df[each] = pd.to_numeric(df[each], downcast="unsigned")
  
  ''' 2) Numeric 정보 담은 변수 생성 과정 '''
  '''2-1 Numeric'''
  # 2-1-1) 각 numeric 관련 변수 생성
  df_numeric_columns = list((df_numeric).columns)
  df_numeric_mean =  df_numeric.mean().round(1)
  df_numeric_std = df_numeric.std().round(1)
  df_numeric_quantile1 = df_numeric.quantile(.25).round(2)
  df_numeric_quantile2 = df_numeric.quantile(.5).round(2)
  df_numeric_quantile3 = df_numeric.quantile(.75).round(2)
  df_numeric_quantile4 = df_numeric.quantile(1).round(2)
  df_numeric_numOfNA = df_numeric.isnull().sum()

  # 2-1-2 모든 numeric 변수들을 담고 있는 종합 Info 변수 생성
  df_numeric_info = pd.DataFrame(index=list(df_numeric.columns)) 

  # 2-1-3 Info 변수에 각 변수 투입
  df_numeric_info.insert(0,'mean',df_numeric_mean)
  df_numeric_info.insert(1,'std',df_numeric_std)
  df_numeric_info.insert(2,'quantile1',df_numeric_quantile1)
  df_numeric_info.insert(2,'quantile2',df_numeric_quantile2)
  df_numeric_info.insert(2,'quantile3',df_numeric_quantile3)
  df_numeric_info.insert(2,'quantile4',df_numeric_quantile4)
  df_numeric_info.insert(3,'numOfNA',df_numeric_numOfNA)
  
  # distribution 데이터 (frequency) 
  distribution_features = []
  interval_features = []
  distribution_features_column = []
  for each in df_numeric.columns:
    dictdata = {'min':float(df_numeric[each].min())}
    dictdata['max'] = float(df_numeric[each].max())
    interval_features.append(dictdata)
      
    distribution_features.append(df_numeric[each].value_counts(bins=10).to_list())
  #   배열 초기화
    dictdata = {}
    distribution_features_column = []
  
  #####################################################
  '''2-2 Category'''
  # 2-2-1) 각 category 관련 변수 생성
  df_categorical_columns = list((df_categorical).columns)
  df_categorical_mostCommon = df_categorical.value_counts().idxmax()
  df_categorical_numOfNA = df_categorical.isnull().sum()

  # 2-2-2) 모든 category 변수들을 담고 있는 종합 Info 변수 생성
  df_categorical_info = pd.DataFrame(index=list(df_categorical.columns)) 

  # 2-2-3) Info 변수에 각 변수 투입
  df_categorical_info.insert(0,'mostCommon',df_categorical_mostCommon)
  df_categorical_info.insert(1,'numOfNA',df_categorical_numOfNA)

  ''' 3) Return '''
  print(distribution_features)


# 반환
  summarizedDF = (df_numeric_info.to_dict(), df_categorical_info.to_dict())
  return  jsonify(df_numeric_info.to_dict(), df_categorical_info.to_dict(),df_numeric_columns,df_categorical_columns,distribution_features, distribution_features,interval_features)
  # return Response(df_numeric_info.to_json(), df_categorical_info.to_json(),df_numeric_columns.to_json(),df_categorical_columns.to_json(), mimetype='application/json')
