import os
import numpy as np
import pandas as pd
from random import *
import json
import joblib
from IPython.display import display


from app import jsonify, Response
import xgboost as xgb
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.model_selection import train_test_split

def runSimulation_ud(observedVariable):
    df_00 = pd.read_csv("./boston_house.csv")

    ''' 1. observedVariable 외 변수들'''
    observedVariable = 'CRIM'

    X = df_00.drop(['MEDV',observedVariable], axis = 1)
    
    X_mean = X.mean().round(2) #그 외 변수의 mean (평균)
    X_std = X.std().round(1)*0.1 #그 외 변수의 std (표준편차)
    X_median = X.median() #그 외 변수의 std (표준편차)

    X_info = pd.DataFrame({'median':X_median,'mean':X_mean.values,'std':X_std.values})
    randNumbers = []
    # 난수를 생성함과 동시에 series로 type converting해서 randNumbers에 삽입
    # randNumbers: series 난수들을 갖고 있는 배열

    for i,v in X_info.iterrows():
        # mean = v[0]
        # std = v[1]
        median = v[0]
        randomized = np.full(5000,median)
        print(randomized)
        randomized = pd.Series(randomized)
        randNumbers.append(randomized)

    X_final = pd.DataFrame(randNumbers)
    # 컬럼과 인덱스 순서 변경
    X_final = X_final.transpose() 
    
    # 컬럼명 지정
    X_final.columns = X.columns

    # category data는 median으로 값 일괄 지정 
    X_final['RAD'] = X['RAD'].median()
    X_final['CHAS'] = X['CHAS'].median()
    # display(X_final)
  

    ''' 2. observedVariable '''
    # df 추출
    df_observedVariable = df_00[observedVariable]
    
    # min & max 추출
    observedVariable_min = df_observedVariable.min()
    observedVariable_max = df_observedVariable.max()

    # random number 생성
    observedVariable_rand = np.random.uniform(observedVariable_min,observedVariable_max,5000)
    observedVariable_final = pd.Series(observedVariable_rand)
    X_final[observedVariable] = observedVariable_final

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
    totalFinal = X_final.sort_values(by='CRIM')
    

    return jsonify({"predicted":totalFinal['MEDV'].tolist(),"randNum":totalFinal[observedVariable].tolist()})