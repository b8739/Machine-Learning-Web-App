# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 13:00:00 2020

@author: s
"""

### PBL-10 : Regression Model - "Boston Housing" data set, 2020-10-29  ###

import os
import pandas as pd
import numpy as np

# import matplotlib
# matplotlib.use("TKAgg")
# import matplotlib.pyplot as plt

# import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

import joblib

from sklearn.model_selection import KFold, GridSearchCV
import xgboost as xgb

from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR


from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

import json
from application import jsonify, Response


def MAPE(y, pred):
    return np.mean(np.abs((y - pred) / y) * 100)


class Algorithm:
    def xgboost(data, splitRatio, modelingRequest):
        ## 01. OPEN DATA & PROCESSING ##

        df_00 = data

        ## EXTRACT X & y SEPARATELY ##
        print(modelingRequest)
        X = df_00[modelingRequest["inputs"]]
        y = df_00[modelingRequest["targets"][0]]
        print(splitRatio)

        ## Valid Data (20%) 사전에 추출 ##

        # startIndex = round(len(df_00)*0.8)

        startIndex = int(
            len(df_00) - (len(df_00) * (int(splitRatio["validation"]) * 0.01))
        )

        endIndex = len(df_00)
        print("startIndex", startIndex)
        print("endIndex", endIndex)

        X_valid = X[startIndex:endIndex]
        y_valid = y[startIndex:endIndex]

        X = X.drop(X.index[startIndex:endIndex])
        y = y.drop(y.index[startIndex:endIndex])

        ## SET 'TRAIN', 'TEST' DATA, TRAIN/TEST RATIO, & 'WAY OF RANDOM SAMPLING' ##
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=123
        )
        # X_test, X_valid, y_test, y_valid = train_test_split(X_test, y_test,test_size=0.5,random_state=123)

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

        # scaler 저장
        # file_name = 'scaler_xgboost.pkl'
        # joblib.dump(scalerX,file_name)

        ## CASE 03. 'XGBOOST' ALGORITHM ##
        # 기존 model
        # 개발 편의성 속성 직접 받지 않고 주석처리
        # xgb_model = xgb.XGBRegressor(n_estimators = 500,
        #                             learning_rate = 0.08,
        #                             gamma = 0.3,
        #                             eta = 0.04,
        #                             subsample = 0.75,
        #                             colsample_bytree = 0.5,
        #                             max_depth = 7)
        parameters = modelingRequest["algorithm"]["parameters"]
        for key, value in parameters.items():
            if parameters[key].find(".") != -1:
                parameters[key] = float(value)
            # 아니라면 (.이 포함되어 있지 않으면) 정수이니 int로 변환
            else:
                parameters[key] = int(value)
        print(parameters[key])

        xgb_model = xgb.XGBRegressor(
            n_estimators=parameters["n_estimators"],
            learning_rate=parameters["learning_rate"],
            gamma=parameters["gamma"],
            eta=parameters["eta"],
            subsample=parameters["subsample"],
            colsample_bytree=parameters["colsample_bytree"],
            max_depth=parameters["max_depth"],
        )

        xgb_model.fit(train_Xn, y_train)

        # xgb.plot_importance(xgb_model)

        xgb_model_predict_test = xgb_model.predict(test_Xn)
        xgb_model_predict_valid = xgb_model.predict(valid_Xn)

        # test result
        try:
            rSquare_test = r2_score(y_test, xgb_model_predict_test)
        except ValueError as e:
            return jsonify(str(e)), 500

        RMSE_test = mean_squared_error(y_test, xgb_model_predict_test) ** 0.5
        MAPE_test = MAPE(y_test, xgb_model_predict_test)

        # formatting (round)
        MAPE_test = str(round(MAPE_test, 2)) + "%"
        rSquare_test = round(rSquare_test, 4)
        RMSE_test = round(RMSE_test, 4)

        # valid result
        rSquare_valid = r2_score(y_valid, xgb_model_predict_valid)
        RMSE_valid = mean_squared_error(y_valid, xgb_model_predict_valid) ** 0.5
        MAPE_valid = MAPE(y_valid, xgb_model_predict_valid)

        # formatting (round)
        MAPE_valid = str(round(MAPE_valid, 2)) + "%"
        rSquare_valid = round(rSquare_valid, 4)
        RMSE_valid = round(RMSE_valid, 4)

        # 반환
        modelingResult = {"test": None, "valid": None}
        modelingResult["test"] = {
            "R_square": rSquare_test,
            "RMSE": RMSE_test,
            "MAPE": MAPE_test,
        }
        modelingResult["valid"] = {
            "R_square": rSquare_valid,
            "RMSE": RMSE_valid,
            "MAPE": MAPE_valid,
        }

        modelingValues = {"test": None, "valid": None}
        modelingValues["test"] = {
            "Actual": y_test.tolist(),
            "Predictive": xgb_model_predict_test.tolist(),
        }
        modelingValues["valid"] = {
            "Actual": y_valid.tolist(),
            "Predictive": xgb_model_predict_valid.tolist(),
        }

        return jsonify(modelingValues, modelingResult)
        # return Response(result.to_json( orient='records'), mimetype='application/json')

    ## 01. OPEN DATA & PROCESSING ##
    def svr(data, splitRatio, modelingRequest):
        df_00 = data

        ## EXTRACT X & y SEPARATELY ##
        X = df_00[modelingRequest["inputs"]]
        y = df_00[modelingRequest["targets"][0]]

        ## Valid Data (20%) 사전에 추출 ##

        # startIndex = round(len(df_00)*0.8)

        startIndex = int(
            len(df_00) - (len(df_00) * (int(splitRatio["validation"]) * 0.01))
        )

        endIndex = len(df_00)
        print("startIndex", startIndex)
        print("endIndex", endIndex)

        X_valid = X[startIndex:endIndex]
        y_valid = y[startIndex:endIndex]

        X = X.drop(X.index[startIndex:endIndex])
        y = y.drop(y.index[startIndex:endIndex])

        ## SET 'TRAIN', 'TEST' DATA, TRAIN/TEST RATIO, & 'WAY OF RANDOM SAMPLING' ##
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=123
        )

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
        parameters = modelingRequest["algorithm"]["parameters"]
        for key, value in parameters.items():
            if parameters[key].isalpha() == True:
                continue
            elif parameters[key].find(".") != -1:
                parameters[key] = float(value)
            # 아니라면 (.이 포함되어 있지 않으면) 정수이니 int로 변환
            else:
                parameters[key] = int(value)

        # svr_model = SVR(kernel = 'rbf',
        #                 C = 100,
        #                 epsilon = 0.1,
        #                 gamma = 0.005)

        svr_model = SVR(
            kernel=parameters["kernel"],
            C=parameters["C"],
            epsilon=parameters["epsilon"],
            gamma=parameters["gamma"],
        )
        # 학습과정 (xn은 normalization을 한 것)

        svr_model.fit(train_Xn, y_train)
        # 예측값
        svr_model_predict_test = svr_model.predict(test_Xn)
        svr_model_predict_valid = svr_model.predict(valid_Xn)

        # test
        rSquare_test = r2_score(y_test, svr_model_predict_test)
        RMSE_test = mean_squared_error(y_test, svr_model_predict_test) ** 0.5
        MAPE_test = MAPE(y_test, svr_model_predict_test)

        # formatting (round)
        MAPE_test = str(round(MAPE_test, 2)) + "%"
        rSquare_test = round(rSquare_test, 4)
        RMSE_test = round(RMSE_test, 4)

        # valid
        rSquare_valid = r2_score(y_valid, svr_model_predict_valid)
        RMSE_valid = mean_squared_error(y_valid, svr_model_predict_valid) ** 0.5
        MAPE_valid = MAPE(y_valid, svr_model_predict_valid)

        # formatting (round)
        MAPE_valid = str(round(MAPE_valid, 2)) + "%"
        rSquare_valid = round(rSquare_valid, 4)
        RMSE_valid = round(RMSE_valid, 4)

        modelingResult = {"test": None, "valid": None}
        modelingResult["test"] = {
            "R_square": rSquare_test,
            "RMSE": RMSE_test,
            "MAPE": MAPE_test,
        }
        modelingResult["valid"] = {
            "R_square": rSquare_valid,
            "RMSE": RMSE_valid,
            "MAPE": MAPE_valid,
        }

        # print(y_test.tolist())
        modelingValues = {"test": None, "valid": None}
        modelingValues["test"] = {
            "Actual": y_test.tolist(),
            "Predictive": svr_model_predict_test.tolist(),
        }
        modelingValues["valid"] = {
            "Actual": y_valid.tolist(),
            "Predictive": svr_model_predict_valid.tolist(),
        }

        return jsonify(modelingValues, modelingResult)

    def rf(data, splitRatio, modelingRequest):
        #### REGRESSION MODEL : "Boston Housing" DATA SET ####

        ## 01. OPEN DATA & PROCESSING ##

        df_00 = data

        ## EXTRACT X & y SEPARATELY ##
        X = df_00[modelingRequest["inputs"]]
        y = df_00[modelingRequest["targets"][0]]

        ## Valid Data (20%) 사전에 추출 ##

        # startIndex = round(len(df_00)*0.8)

        startIndex = int(
            len(df_00) - (len(df_00) * (int(splitRatio["validation"]) * 0.01))
        )

        endIndex = len(df_00)
        print("startIndex", startIndex)
        print("endIndex", endIndex)

        X_valid = X[startIndex:endIndex]
        y_valid = y[startIndex:endIndex]

        X = X.drop(X.index[startIndex:endIndex])
        y = y.drop(y.index[startIndex:endIndex])

        ## SET 'TRAIN', 'TEST' DATA, TRAIN/TEST RATIO, & 'WAY OF RANDOM SAMPLING' ##
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=123
        )
        print(y_test.tolist())
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

        parameters = modelingRequest["algorithm"]["parameters"]
        for key, value in parameters.items():
            if parameters[key].find(".") != -1:
                parameters[key] = float(value)
            # 아니라면 (.이 포함되어 있지 않으면) 정수이니 int로 변환
            else:
                parameters[key] = int(value)
        print(parameters[key])

        ## CASE 02. 'RANDOM FOREST' ALGORITHM ##
        # rf_model = RandomForestRegressor(n_estimators = 800,
        #                                 min_samples_split = 3)

        rf_model = RandomForestRegressor(
            n_estimators=parameters["n_estimators"],
            min_samples_split=parameters["min_samples_split"],
        )

        rf_model.fit(train_Xn, y_train)
        rf_model_predict_test = rf_model.predict(test_Xn)
        rf_model_predict_valid = rf_model.predict(valid_Xn)

        rSquare_test = r2_score(y_test, rf_model_predict_test)
        RMSE_test = mean_squared_error(y_test, rf_model_predict_test) ** 0.5
        MAPE_test = MAPE(y_test, rf_model_predict_test)

        # formatting (round)
        MAPE_test = str(round(MAPE_test, 2)) + "%"
        rSquare_test = round(rSquare_test, 4)
        RMSE_test = round(RMSE_test, 4)

        # valid result
        rSquare_valid = r2_score(y_valid, rf_model_predict_valid)
        RMSE_valid = mean_squared_error(y_valid, rf_model_predict_valid) ** 0.5
        MAPE_valid = MAPE(y_valid, rf_model_predict_valid)

        # formatting (round)
        MAPE_valid = str(round(MAPE_valid, 2)) + "%"
        rSquare_valid = round(rSquare_valid, 4)
        RMSE_valid = round(RMSE_valid, 4)

        # 반환
        modelingResult = {"test": None, "valid": None}
        modelingResult["test"] = {
            "R_square": rSquare_test,
            "RMSE": RMSE_test,
            # "MAPE": MAPE_test,
        }
        modelingResult["valid"] = {
            "R_square": rSquare_valid,
            "RMSE": RMSE_valid,
            # "MAPE": MAPE_valid,
        }

        modelingValues = {"test": None, "valid": None}
        modelingValues["test"] = {
            "Actual": y_test.tolist(),
            "Predictive": rf_model_predict_test.tolist(),
        }
        modelingValues["valid"] = {
            "Actual": y_valid.tolist(),
            "Predictive": rf_model_predict_valid.tolist(),
        }

        return jsonify(modelingValues, modelingResult)
