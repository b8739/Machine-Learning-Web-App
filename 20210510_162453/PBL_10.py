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
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

def MAPE(y, pred):
  return np.mean(np.abs((y-pred)/y)*100)

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


## 02. BUILD REGRESSION MODEL ##

## CASE 01. 'SVR' ALGORITHM ##

## Grid Search ##
param={'C':[1, 5, 10, 20, 40, 100, 1000],
      'gamma':[.0001, .005, .05, .1, .25, .5, 1]}
GS = GridSearchCV(SVR(kernel='rbf'),param, cv = 5)
GS.fit(train_Xn, y_train)
print(GS.best_params_)
print(GS.best_score_)


svr_model = SVR(kernel = 'rbf', 
                C = 100, 
                epsilon = 0.1, 
                gamma = 0.005)
# 학습과정 (xn은 normalization을 한 것)
svr_model.fit(train_Xn, y_train)
# 예측값
svr_model_predict = svr_model.predict(test_Xn)

print('R_square of SVR :', r2_score(y_test, svr_model_predict))
print('RMSE of SVR :', mean_squared_error(y_test, svr_model_predict)**0.5)
print('MAPE of SVR :', MAPE(y_test, svr_model_predict))

## VISUALIZE THE RESULTS ##
y0 = pd.DataFrame(range(len(y_test)))
y1 = pd.DataFrame(y_test)
y1 = y1.reset_index(drop = True)
y2 = pd.DataFrame(svr_model_predict)

result = pd.concat([y0, y1, y2], axis = 1)
result.columns = ['no', 'Actual', 'Predictive']

## Graphs ##
plt.style.use('bmh')
# plt.style.use('ggplot')
plt.figure(figsize = (12, 5))
plt.plot(result.iloc[:, 1], color = 'dodgerblue', alpha = 0.3, marker = 'o', linewidth = 0.5)
plt.plot(result.iloc[:, 2], color = 'brown', alpha = 0.4, marker = 'o', linewidth = 0.5)
plt.title('Actual vs. Predictive : SVR')
plt.show()



## CASE 02. 'RANDOM FOREST' ALGORITHM ##

rf_model = RandomForestRegressor(n_estimators = 800, 
                                 min_samples_split = 3)

rf_model.fit(train_Xn, y_train)
rf_model_predict = rf_model.predict(test_Xn)

print('R_square of RF :', r2_score(y_test, rf_model_predict))
print('RMSE of RF :', mean_squared_error(y_test, rf_model_predict)**0.5)
print('MAPE of RF :', MAPE(y_test, rf_model_predict))

## VISUALIZE THE RESULTS ##
z0 = pd.DataFrame(range(len(y_test)))
z1 = pd.DataFrame(y_test)
z1 = z1.reset_index(drop = True)
z2 = pd.DataFrame(rf_model_predict)

result = pd.concat([z0, z1, z2], axis = 1)
result.columns = ['no', 'Actual', 'Predictive']

## Graphs ##
plt.style.use('bmh')
# plt.style.use('ggplot')
plt.figure(figsize = (12, 5))
plt.plot(result.iloc[:, 1], color = 'dodgerblue', alpha = 0.3, marker = 'o', linewidth = 0.5)
plt.plot(result.iloc[:, 2], color = 'brown', alpha = 0.4, marker = 'o', linewidth = 0.5)
plt.title('Actual vs. Predictive : RF')
plt.show()



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

print('R_square of XGB :', r2_score(y_test, xgb_model_predict))
print('RMSE of XGB :', mean_squared_error(y_test, xgb_model_predict)**0.5)
print('MAPE of XGB :', MAPE(y_test, xgb_model_predict))

## VISUALIZE THE RESULTS ##
w0 = pd.DataFrame(range(len(y_test)))
w1 = pd.DataFrame(y_test)
w1 = w1.reset_index(drop = True)
w2 = pd.DataFrame(xgb_model_predict)

result = pd.concat([w0, w1, w2], axis = 1)
result.columns = ['no', 'Actual', 'Predictive']

## Graphs ##
plt.style.use('bmh')
# plt.style.use('ggplot')
plt.figure(figsize = (12, 5))
plt.plot(result.iloc[:, 1], color = 'dodgerblue', alpha = 0.3, marker = 'o', linewidth = 0.5)
plt.plot(result.iloc[:, 2], color = 'brown', alpha = 0.4, marker = 'o', linewidth = 0.5)
plt.title('Actual vs. Predictive : XGB')
plt.show()






## FOR XGB MODEL, WE CAN SELECT THE IMPORTANT FEATURES TO BE USED FOR THE MODEL : 변수가 많은 경우 사용 ##
cols_to_fit = train_X.columns

feature_imp = pd.DataFrame(sorted(zip(xgb_model.feature_importances_, cols_to_fit)), 
                           columns = ['Value', 'Feature'])
feature_imp = feature_imp.sort_values(by = ['Value'], axis = 0, ascending = False)

n = 7
vars_0 = list(feature_imp['Feature'])[:n]

## NEW FEATURES SELECTED ##

train_Xs = X_train.loc[ :, vars_0]
test_Xs = X_test.loc[ :, vars_0]

## NORMALIZATION ##
scalerX = StandardScaler()
scalerX.fit(train_Xs)
train_X_imp = scalerX.transform(train_Xs)
test_X_imp = scalerX.transform(test_Xs)


xgb_model = xgb.XGBRegressor(n_estimators = 500, 
                             learning_rate = 0.08, 
                             gamma = 0.3, 
                             eta = 0.04,
                             subsample = 0.75,
                             colsample_bytree = 0.5, 
                             max_depth = 7)

xgb_model.fit(train_Xs, y_train)

xgb_model_predict = xgb_model.predict(test_Xs)

print('R_square of XGB :', r2_score(y_test, xgb_model_predict))
print('RMSE of XGB :', mean_squared_error(y_test, xgb_model_predict)**0.5)
print('MAPE of XGB :', MAPE(y_test, xgb_model_predict))

## VISUALIZE THE RESULTS ##
w0 = pd.DataFrame(range(len(y_test)))
w1 = pd.DataFrame(y_test)
w1 = w1.reset_index(drop = True)
w2 = pd.DataFrame(xgb_model_predict)

result = pd.concat([w0, w1, w2], axis = 1)
result.columns = ['no', 'Actual', 'Predictive']

## Graphs ##
plt.style.use('bmh')
# plt.style.use('ggplot')
plt.figure(figsize = (12, 5))
plt.plot(result.iloc[:, 1], color = 'dodgerblue', alpha = 0.3, marker = 'o', linewidth = 0.5)
plt.plot(result.iloc[:, 2], color = 'brown', alpha = 0.4, marker = 'o', linewidth = 0.5)
plt.title('Actual vs. Predictive : XGB')
plt.show()






## XGBOOST GRID SEARCH ##

x_model = xgb.XGBRegressor()

param_grid={'booster' :['gbtree'],
                 'silent':[True],
                 'max_depth':[5,6,8],
                 'min_child_weight':[1,3,5],
                 'gamma':[0.0,1,2,3],
                 'nthread':[4],
                 'colsample_bytree':[0.5,0.8],
                 'colsample_bylevel':[0.9],
                 'n_estimators':[50],
                 'objective':['binary:logistic'],
                 'random_state':[2]}





xgb.XGBRegressor(n_estimators = 500, 
                             learning_rate = 0.08, 
                             gamma = 0.3, 
                             eta = 0.04,
                             subsample = 0.75,
                             colsample_bytree = 0.5, 
                             max_depth = 7)


































