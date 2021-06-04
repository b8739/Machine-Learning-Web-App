# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 13:00:00 2020

@author: s
"""

### PBL-10 : Regression Model - "Boston Housing" data set, 2020-10-29  ### 

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

from sklearn.svm import SVR
from sklearn.model_selection import KFold, GridSearchCV

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

import json
from app import jsonify, Response


def MAPE(y, pred):
  return np.mean(np.abs((y-pred)/y)*100)

#### REGRESSION MODEL : "Boston Housing" DATA SET ####

## 01. OPEN DATA & PROCESSING ##
def svr(modelingOption):
  df_00 = pd.read_csv("./boston_house.csv")

  # df_00 = df_00.drop('Unnamed: 0', axis = 1)

  ## EXTRACT X & y SEPARATELY ##
  X = df_00.drop('MEDV', axis = 1)
  y = df_00['MEDV']

  ## Valid Data (20%) 사전에 추출 ##
  startIndex = round(len(df_00)*0.8)
  X_valid = X[startIndex:]
  y_valid = y[startIndex:]

  X= X.drop(X.index[startIndex:])
  y= y.drop(y.index[startIndex:])

  ## SET 'TRAIN', 'TEST' DATA, TRAIN/TEST RATIO, & 'WAY OF RANDOM SAMPLING' ##
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 123)

  # test
  train_X = X_train 
  test_X = X_test

  # valid
  valid_X = X_valid

  ## NORMALIZATION ##
  scalerX = StandardScaler()
  scalerX.fit(train_X)
  train_Xn = scalerX.transform(train_X)
  test_Xn = scalerX.transform(test_X)
  valid_Xn = scalerX.transform(valid_X)


  # ## 02. BUILD REGRESSION MODEL ##

  # ## CASE 01. 'SVR' ALGORITHM ##

  ## Grid Search ##
  # param={'C':[1, 5, 10, 20, 40, 100, 1000],
  #       'gamma':[.0001, .005, .05, .1, .25, .5, 1]}
  # GS = GridSearchCV(SVR(kernel='rbf'),param, cv = 5)
  # GS.fit(train_Xn, y_train)
  # print(GS.best_params_)
  # print(GS.best_score_)


  svr_model = SVR(kernel = 'rbf', 
                  C = 100, 
                  epsilon = 0.1, 
                  gamma = 0.005)

  # svr_model = SVR(kernel = modelingOption[0], 
  #                 C = modelingOption[1], 
  #                 epsilon = modelingOption[2], 
  #                 gamma = modelingOption[3])
  # 학습과정 (xn은 normalization을 한 것)

  svr_model.fit(train_Xn, y_train)
  # 예측값
  svr_model_predict_test = svr_model.predict(test_Xn)
  svr_model_predict_valid = svr_model.predict(valid_Xn)
  
  # test
  rSquare_test = r2_score(y_test, svr_model_predict_test)
  RMSE_test = mean_squared_error(y_test, svr_model_predict_test)**0.5
  MAPE_test = MAPE(y_test, svr_model_predict_test)

  # formatting (round)
  MAPE_test = str(round(MAPE_test,2))+'%'
  rSquare_test = round(rSquare_test,4)
  RMSE_test = round(RMSE_test,4)

  # valid
  rSquare_valid = r2_score(y_valid, svr_model_predict_valid)
  RMSE_valid = mean_squared_error(y_valid, svr_model_predict_valid)**0.5
  MAPE_valid = MAPE(y_valid, svr_model_predict_valid)

  # formatting (round)
  MAPE_valid = str(round(MAPE_valid,2))+'%'
  rSquare_valid = round(rSquare_valid,4)
  RMSE_valid = round(RMSE_valid,4)


  modelingResult = {'test':None, 'valid':None}
  modelingResult['test'] = {'R_square of SVR': rSquare_test, 'RMSE_test of SVR': RMSE_test,'MAPE of SVR': MAPE_test}
  modelingResult['valid'] = {'R_square of SVR': rSquare_valid, 'RMSE_test of SVR': RMSE_valid,'MAPE of SVR': MAPE_valid}

  # print(y_test.tolist())
  modelingValues = {'test':None, 'valid':None}
  modelingValues['test'] = {'Actual':y_test.tolist(),'Predictive':svr_model_predict_test.tolist()}
  modelingValues['valid'] = {'Actual':y_valid.tolist(),'Predictive':svr_model_predict_valid.tolist()}
  return jsonify(modelingValues,modelingResult)