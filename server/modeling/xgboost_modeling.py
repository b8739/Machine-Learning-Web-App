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
import xgboost as xgb

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

import json
from app import jsonify, Response

def MAPE(y, pred):
  return np.mean(np.abs((y-pred)/y)*100)

def xgboost(modelingOption):
    #### REGRESSION MODEL : "Boston Housing" DATA SET ####

    ## 01. OPEN DATA & PROCESSING ##

    df_00 = pd.read_csv("./boston_house.csv")

    # df_00 = df_00.drop('Unnamed: 0', axis = 1)

    ## EXTRACT X & y SEPARATELY ##
    X = df_00.drop('MEDV', axis = 1)
    y = df_00['MEDV']

    ## SET 'TRAIN', 'TEST' DATA, TRAIN/TEST RATIO, & 'WAY OF RANDOM SAMPLING' ##
    # 두 단계에 거쳐서 Dataset을 Train, Test, Validation (6:2:2)로 나눔
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state = 123)
    X_test, X_valid, y_test, y_valid = train_test_split(X_test, y_test,test_size=0.5,random_state=123)

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

    ## CASE 03. 'XGBOOST' ALGORITHM ##
    # 기존 model

    # xgb_model = xgb.XGBRegressor(n_estimators = 500, 
    #                             learning_rate = 0.08, 
    #                             gamma = 0.3, 
    #                             eta = 0.04,
    #                             subsample = 0.75,
    #                             colsample_bytree = 0.5, 
    #                             max_depth = 7)
    xgb_model = xgb.XGBRegressor(n_estimators = modelingOption[0], 
                              learning_rate = modelingOption[1], 
                              gamma = modelingOption[2], 
                              eta = modelingOption[3],
                              subsample = modelingOption[4],
                              colsample_bytree = modelingOption[5], 
                              max_depth = modelingOption[6])

    xgb_model.fit(train_Xn, y_train)

    xgb.plot_importance(xgb_model)

    xgb_model_predict_test = xgb_model.predict(test_Xn)
    xgb_model_predict_valid = xgb_model.predict(valid_Xn)

    # test result
    rSquare_test = r2_score(y_test, xgb_model_predict_test)
    RMSE_test = mean_squared_error(y_test, xgb_model_predict_test)**0.5
    MAPE_test = MAPE(y_test, xgb_model_predict_test)

    # valid result
    rSquare_test = r2_score(y_valid, xgb_model_predict_valid)
    RMSE_test = mean_squared_error(y_valid, xgb_model_predict_valid)**0.5
    MAPE_test = MAPE(y_valid, xgb_model_predict_valid)

    ## VISUALIZE THE RESULTS ##
    # w0 = pd.DataFrame(range(len(y_test)))
    # w1 = pd.DataFrame(y_test)
    # w1 = w1.reset_index(drop = True)
    # w2 = pd.DataFrame(xgb_model_predict_test)

    # result = pd.concat([w0,w1], axis = 1)
    # result2 = pd.concat([w0,w2], axis = 1)
    # result.columns = ['x','y']
    # result2.columns = ['x','y']

    # 반환
    modelingResult = {'R_square of XGB': rSquare_test, 'RMSE_test of XGB': RMSE_test,'MAPE of XGB': MAPE_test}

    # print(y_test.tolist())
    modelingValues = {'test':None, 'valid':None}
    modelingValues['test'] = {'Actual':y_test.tolist(),'Predictive':xgb_model_predict_test.tolist()}
    modelingValues['valid'] = {'Actual':y_valid.tolist(),'Predictive':xgb_model_predict_valid.tolist()}
    return jsonify(modelingValues,modelingResult)
    # return Response(result.to_json( orient='records'), mimetype='application/json')
