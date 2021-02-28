# from app import df

import pandas as pd 
import numpy as np 
import os
import json
import matplotlib

df = pd.read_csv('./static/uploadsDB/pima-indians-diabetes.csv')
# 0) df type에 따라서 나누기 (categorical/numeric)

# categorical 있는지 검사
numOfCategoricalData = len(df.select_dtypes(include = ['object']).columns.tolist())
#  전부 NUMERIC인 상황
if (numOfCategoricalData == 0 ): 
  df_numeric = df.copy()
  # 1) numeric 변수 생성
  # df_numeric_type = df_numeric.dtypes
  df_numeric_columns = list((df_numeric).columns)
  df_numeric_mean =  df_numeric.mean().round(3)
  df_numeric_std = df_numeric.std().round(3)
  df_numeric_quantile = df_numeric.quantile()
  df_numeric_numOfNA = df_numeric.isnull().sum()

  # 2) numeric Dataframe 생성
  df_numeric_info = pd.DataFrame(index=list(df_numeric.columns)) 

  # 3) df에 투입
  # df_numeric_info.insert(0,'type',df_numeric_type)
  df_numeric_info.insert(0,'mean',df_numeric_mean)
  df_numeric_info.insert(1,'std',df_numeric_std)
  df_numeric_info.insert(2,'quantile',df_numeric_quantile)
  df_numeric_info.insert(3,'numOfNA',df_numeric_numOfNA)
  return 
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
  summarizedDF = [df_numeric_info,df_categorical_info]
  print(type(summarizedDF))





