import os
import numpy as np
import pandas as pd
from random import *
import json
import joblib
from IPython.display import display
import math


from app import jsonify, Response
import xgboost as xgb
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.model_selection import train_test_split

def randn_bm(min,max,skew):
    u = 0
    v = 0
    
    while u == 0:
        u = np.random.rand()
    while v == 0:
        v = np.random.rand()
    num = math.sqrt(-2.0*math.log(u)) * math.cos(2.0*math.pi*v)

    num = num/10.0+0.5
    if num>1 or num <0:
        num = randn_bm(min,max,skew)
    num = math.pow(num,skew)
    num *= max - min
    num +=min
    return num

def getSimulationResult(observedVariable,rangeInfo):
    # csv 데이터 불러오기
    df_00 = pd.read_csv("./boston_house.csv")
    X = df_00.drop(['MEDV'], axis = 1)
    observedVariable = 'CRIM'
    # rand number 생성
    randNumbers = []
    for key,value in rangeInfo.items():
        intervals = {}
        # intervals['min'] = value['interval']['min']
        # intervals['max'] = value['interval']['max']
        for nestedKey,nestedValue in value['interval'].items():
            intervalValue = value['interval'][nestedKey]
            if isinstance(intervalValue, str) == True:
                intervals[nestedKey] = int(intervalValue)
            else:
                intervals[nestedKey] = intervalValue
        randomized = []
        #normal 일 때
        if value['method'] == 'normal': 
            for i in range(1000):
                randValue = round(randn_bm(intervals['min'],intervals['max'],1),3)
                randomized.append(randValue)
            randomized= pd.Series(randomized)
            randNumbers.append(randomized)
        # manual 일 때
        else: 
            randomized=(np.random.uniform(intervals['min'],intervals['max'],1000).round(2))
            randomized= pd.Series(randomized)
            randNumbers.append(randomized)
    X_final = pd.DataFrame(randNumbers)

    X_final = X_final.transpose() 
    X_final.columns = X.columns


    ## NORMALIZATION (저장된 scaler)##
    file_name = 'scaler_xgboost.pkl'
    scalerX= joblib.load(file_name) 
    X_final_n = scalerX.transform(X_final)

    '''modeling 시작'''
    
    # model parameter (sql에서 가져와야 할듯?)
    xgb_model = xgb.XGBRegressor(n_estimators = 500, 
                            learning_rate = 0.08, 
                            gamma = 0.3, 
                            eta = 0.04,
                            subsample = 0.75,
                            colsample_bytree = 0.5, 
                            max_depth = 7)
    
    # 저장된 모델 불러오기 (모델을 harddisk말고 mysql에 저장해야 함)
    xgb_model.load_model("model.json")

    # model 예측 
    xgb_model_predict_x = xgb_model.predict(X_final_n)

    # MEDV와 CRIM을 동일한 df에 넣어야지 함께 정렬됨 
    X_final['MEDV'] = pd.Series(xgb_model_predict_x)

    # 오름차순으로 정렬 (증감 변화를 확인하는것이 목적이기 때문)
    totalFinal = X_final.sort_values(by=observedVariable)

    return jsonify({"predicted":totalFinal['MEDV'].tolist(),"randNum":totalFinal[observedVariable].tolist()})