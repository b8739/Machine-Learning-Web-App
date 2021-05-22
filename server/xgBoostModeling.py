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

from sklearn.svm import SVR
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

import json
from app import jsonify, Response

def MAPE(y, pred):
  return np.mean(np.abs((y-pred)/y)*100)

def xgboost():
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


    ## CASE 03. 'XGBOOST' ALGORITHM ##

    xgb_model = xgb.XGBRegressor(n_estimators = 500, 
                                learning_rate = 0.08, 
                                gamma = 0.3, 
                                eta = 0.04,
                                subsample = 0.75,
                                colsample_bytree = 0.5, 
                                max_depth = 7)

    xgb_model.fit(train_Xn, y_train)

    xgb.plot_importance(xgb_model)

    xgb_model_predict = xgb_model.predict(test_Xn)

    rSquare = r2_score(y_test, xgb_model_predict)
    RMSE = mean_squared_error(y_test, xgb_model_predict)**0.5
    MAPE1 = MAPE(y_test, xgb_model_predict)


    print('R_square of XGB :', r2_score(y_test, xgb_model_predict))
    print('RMSE of XGB :', mean_squared_error(y_test, xgb_model_predict)**0.5)
    print('MAPE of XGB :', MAPE(y_test, xgb_model_predict))

    # 반환
    xgBoostModelingResult = {'R_square of XGB': rSquare, 'RMSE of XGB': RMSE,'MAPE of XGB': MAPE1}
    return  jsonify(xgBoostModelingResult)
