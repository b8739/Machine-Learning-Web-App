# from app import df

import pandas as pd 
import numpy as np 
import os
import json
import matplotlib
from app import jsonify

def summarizeData(df):
  print(df.dtypes)
  category_features = []
  threshold = 10
  for each in df.columns:
    if df[each].nunique() < threshold:
        category_features.append(each)
    elif df[each].dtypes == 'object' or df[each].dtypes == 'ID':
        category_features.append(each)

  for each in category_features:
    df[each] = df[each].astype('category')

  # 0) df type에 따라서 나누기 (categorical/numeric)
  df_numeric = df.select_dtypes(exclude = ['category']).copy()
  df_categorical = df.select_dtypes(include = ['category'] ).copy()
  
  # 1) numeric 변수 생성
  # df_numeric_type = df_numeric.dtypes
  df_numeric_columns = list((df_numeric).columns)
  df_numeric_mean =  df_numeric.mean().round(1)
  df_numeric_std = df_numeric.std().round(1)
  df_numeric_quantile = df_numeric.quantile().round(1)
  df_numeric_numOfNA = df_numeric.isnull().sum()

  # 2) numeric Dataframe 생성
  df_numeric_info = pd.DataFrame(index=list(df_numeric.columns)) 

  # 3) df에 투입
  # df_numeric_info.insert(0,'type',df_numeric_type)
  df_numeric_info.insert(0,'mean',df_numeric_mean)
  df_numeric_info.insert(1,'std',df_numeric_std)
  df_numeric_info.insert(2,'quantile',df_numeric_quantile)
  df_numeric_info.insert(3,'numOfNA',df_numeric_numOfNA)

  #####################################################

  # 1) categorical 변수 생성
  df_categorical_columns = list((df_categorical).columns)
  df_categorical_mostCommon = df_categorical.value_counts().idxmax()
  df_categorical_numOfNA = df_categorical.isnull().sum()

  # 2) categorical dataframe 생성
  df_categorical_info = pd.DataFrame(index=list(df_categorical.columns)) 

  # 3) categorical 변수 df에 투입
  df_categorical_info.insert(0,'mostCommon',df_categorical_mostCommon)
  df_categorical_info.insert(1,'numOfNA',df_categorical_numOfNA)

# 반환
  summarizedDF = (df_numeric_info.to_dict(), df_categorical_info.to_dict())
  return  jsonify(df_numeric_info.to_dict(), df_categorical_info.to_dict(),df_numeric_columns,df_categorical_columns)