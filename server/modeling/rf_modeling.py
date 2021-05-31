# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 13:00:00 2020

@author: s
"""

### PBL-10 : Regression Model - "Boston Housing" data set, 2020-10-29  ### 

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt

import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler


from sklearn.model_selection import KFold, GridSearchCV
from sklearn.ensemble import RandomForestRegressor


from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

import json
from app import jsonify, Response

def MAPE(y, pred):
  return np.mean(np.abs((y-pred)/y)*100)

def rf(modelingOption):
  #### REGRESSION MODEL : "Boston Housing" DATA SET ####

  ## 01. OPEN DATA & PROCESSING ##

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

  ## CASE 02. 'RANDOM FOREST' ALGORITHM ##

  # rf_model = RandomForestRegressor(n_estimators = 800, 
  #                                 min_samples_split = 3)

  rf_model = RandomForestRegressor(n_estimators = modelingOption[0], 
                                  min_samples_split = modelingOption[1])

  rf_model.fit(train_Xn, y_train)
  rf_model_predict = rf_model.predict(test_Xn)

  rSquare = r2_score(y_test, rf_model_predict)
  RMSE = mean_squared_error(y_test, rf_model_predict)**0.5
  MAPE1 = MAPE(y_test, rf_model_predict)

    # formatting (round)
  MAPE1 = str(round(MAPE1,2))+'%'
  rSquare = round(rSquare,4)
  RMSE = round(RMSE,4)

  print('R_square of RF :', rSquare)
  print('RMSE of RF :', RMSE)
  print('MAPE of RF :',MAPE1)

  ## VISUALIZE THE RESULTS ##
  z0 = pd.DataFrame(range(len(y_test)))
  z1 = pd.DataFrame(y_test)
  z1 = z1.reset_index(drop = True)
  z2 = pd.DataFrame(rf_model_predict)

  # result = pd.concat([z0, z1, z2], axis = 1)
  # result.columns = ['no', 'Actual', 'Predictive']

  # ## Graphs ##
  # plt.style.use('bmh')
  # # plt.style.use('ggplot')
  # plt.figure(figsize = (12, 5))
  # plt.plot(result.iloc[:, 1], color = 'dodgerblue', alpha = 0.3, marker = 'o', linewidth = 0.5)
  # plt.plot(result.iloc[:, 2], color = 'brown', alpha = 0.4, marker = 'o', linewidth = 0.5)
  # plt.title('Actual vs. Predictive : RF')
  # plt.show()

  # 반환
  modelingResult = {'R_square of RF': rSquare, 'RMSE of RF': RMSE,'MAPE of RF': MAPE1}

  # print(y_test.tolist())
  chartData = {'Actual':y_test.tolist(),'Predictive':rf_model_predict.tolist()}
  return jsonify(chartData,modelingResult)