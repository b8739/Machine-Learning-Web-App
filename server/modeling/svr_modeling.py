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

  ## SET 'TRAIN', 'TEST' DATA, TRAIN/TEST RATIO, & 'WAY OF RANDOM SAMPLING' ##
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 123)

  train_X = X_train 
  test_X = X_test

  ## NORMALIZATION ##
  scalerX = StandardScaler()
  scalerX.fit(train_X)
  train_Xn = scalerX.transform(train_X)
  test_Xn = scalerX.transform(test_X)


  # ## 02. BUILD REGRESSION MODEL ##

  # ## CASE 01. 'SVR' ALGORITHM ##

  ## Grid Search ##
  # param={'C':[1, 5, 10, 20, 40, 100, 1000],
  #       'gamma':[.0001, .005, .05, .1, .25, .5, 1]}
  # GS = GridSearchCV(SVR(kernel='rbf'),param, cv = 5)
  # GS.fit(train_Xn, y_train)
  # print(GS.best_params_)
  # print(GS.best_score_)


  # svr_model = SVR(kernel = 'rbf', 
  #                 C = 100, 
  #                 epsilon = 0.1, 
  #                 gamma = 0.005)

  svr_model = SVR(kernel = modelingOption[0], 
                  C = modelingOption[1], 
                  epsilon = modelingOption[2], 
                  gamma = modelingOption[3])
  # 학습과정 (xn은 normalization을 한 것)
  svr_model.fit(train_Xn, y_train)
  # 예측값
  svr_model_predict = svr_model.predict(test_Xn)

  rSquare = r2_score(y_test, svr_model_predict)
  RMSE = mean_squared_error(y_test, svr_model_predict)**0.5
  MAPE1 = MAPE(y_test, svr_model_predict)

  print('R_square of SVR :', rSquare)
  print('RMSE of SVR :', RMSE)
  print('MAPE of SVR :', MAPE1)

  ## VISUALIZE THE RESULTS ##
  y0 = pd.DataFrame(range(len(y_test)))
  y1 = pd.DataFrame(y_test)
  y1 = y1.reset_index(drop = True)
  y2 = pd.DataFrame(svr_model_predict)

  # result = pd.concat([y0, y1, y2], axis = 1)
  # result.columns = ['no', 'Actual', 'Predictive']

  ## Graphs ##
  # plt.style.use('bmh')
  # # plt.style.use('ggplot')
  # plt.figure(figsize = (12, 5))
  # plt.plot(result.iloc[:, 1], color = 'dodgerblue', alpha = 0.3, marker = 'o', linewidth = 0.5)
  # plt.plot(result.iloc[:, 2], color = 'brown', alpha = 0.4, marker = 'o', linewidth = 0.5)
  # plt.title('Actual vs. Predictive : SVR')
  # plt.show()

  # 반환
  modelingResult = {'R_square of SVR': rSquare, 'RMSE of SVR': RMSE,'MAPE of SVR': MAPE1}

  # print(y_test.tolist())
  chartData = {'Actual':y_test.tolist(),'Predictive':svr_model_predict.tolist()}
  return jsonify(chartData,modelingResult)