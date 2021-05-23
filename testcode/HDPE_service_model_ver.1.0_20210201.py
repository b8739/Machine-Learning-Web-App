# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 17:21:57 2020
@author: in02421

************      Can Start from 251 Line      ******************************** 
"""

import os
import pandas as pd 
import numpy as np 
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime, timedelta, date
import time

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.linear_model import LinearRegression, Lasso, LassoCV, ElasticNet, ElasticNetCV
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor 
import xgboost as xgb
import math


def NaNRemove(data):
    for i in range(len(list(data.columns))):
        data = data.dropna(subset=[data.columns[i]], how='any')
    data.index = range(len(data.index))
    return data

def MAPE(y, pred):
    return np.mean(np.abs((y-pred)/y)*100)

""" Historam : Select df, start_Col_num #, end_Col_num, & fraction """
def hist_plot(data, st_col_num, end_col_num, fraction=0.05, bin_num=30):
    s = data.iloc[:, st_col_num:(end_col_num+1)]
    n = s.shape[1]
    plt.figure(figsize=(n*3, 3))
    for i in range(st_col_num-st_col_num, end_col_num-st_col_num+1) :
        temp = s.iloc[:, i].sample(frac=fraction)
        plt.subplot(1, n, (i+1))
        
        plt.title(s.columns[i])
        plt.hist(temp, bins=bin_num)
        plt.subplots_adjust(bottom=0.1, wspace=0.4, hspace=0.4)
    return plt.show()

#hist_plot(df_0, 3, 8)

""" Time-series graph using column number """
def ts_plot(data, col_num): # Time-series graph using column number
    data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S')
    d_ = data[(data['time'].dt.minute==0) & 
              (data['time'].dt.second==0)] #Because of memory, filtered "hourly data"
    iqr = d_.iloc[:, col_num].quantile(0.75) - d_.iloc[:, col_num].quantile(0.25)
    plt.figure(figsize=(10, 4))
    plt.style.use('default')
    plt.title(d_.columns[col_num], fontsize=14)
    plt.scatter(d_['time'], d_.iloc[:, col_num], s=1, color = 'dodgerblue', alpha = 0.5)
    axes = plt.gca()
    axes.yaxis.grid()  
    return plt.show()

""" Time-series graph using column name """
def ts_plot_n(data, col_name): # Time-series graph using column name
    data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S')
    d_ = data[(data['time'].dt.minute==0) & 
              (data['time'].dt.second==0)] #Because of memory, filtered "hourly data"
    plt.figure(figsize=(10, 4))
    plt.style.use('default')
    plt.title(col_name, fontsize=14)
    plt.scatter(d_['time'], d_[col_name], s=1, color = 'brown', alpha = 0.5)
#    plt.ylim([0, 1])
#    plt.xlim(['2018-01-01', '2018-03-30'])
    axes = plt.gca()
    axes.yaxis.grid()  
    return plt.show()

""" Time-series graph using column name & modify y-axis (y_min, y_max) """
def ts_plot_n2(data, col_name, y_min, y_max): # Time-series graph using column name
    data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S')
    d_ = data[(data['time'].dt.minute==0) & 
              (data['time'].dt.second==0)] #Because of memory, filtered "hourly data"
    plt.figure(figsize=(10, 4))
    plt.style.use('default')
    plt.title(col_name, fontsize=14)
    plt.scatter(d_['time'], d_[col_name], s=1, color = 'brown', alpha = 0.5)
    plt.ylim([y_min, y_max])
#    plt.xlim(['2018-01-01', '2018-03-30'])
    axes = plt.gca()
    axes.yaxis.grid()  
    return plt.show()

## 화면에 표시되는 행과 열의 수 조정
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)


## Set working Directory ##
os.chdir('C:/GC_POLYMER_2')


''' ###   2021-01-06 : OPEN THE INTEGRATED DATA SET ########################### '''

#### 01. OPEN RTDB DATA SET : 1 min. interval #########################################
df_00 = pd.read_csv('C:/GC_POLYMER_2/data_final/data_all_1min_201221.csv')
df_00 = df_00.drop("Unnamed: 0", axis = 1)
df_00['time'] = pd.to_datetime(df_01['time'], format='%Y-%m-%d %H:%M:%S')


## EDA through Graphs ##
ts_plot(df_00, 10)
hist_plot(df_00, 1, 5, 0.05)

## DELETED UNNECESSARY TAGS ##

df_01 = df_00.drop(['PE02AI2222E2', 'PE02AI2222F1', 'PE02FI2233', ## Modified on 2021-01-10
                    'PE02FI2253', 'PE02FI2651', 'PE02FIC2216C', 
                    'PE02FIC2222', 'PE02FIC2223', 'PE02FIC2231B', 'PE02FIC2232', 'PE02FIC2243', 'PE02FIC2251B', 
                    'PE02FIC2252', 'PE02FIC2255', 'PE02NU2003', 'PE02PDI2221', 'PE02PDI2241', 
                    'PE02PI2212', 'PE02PI2251', 'PE02PIC2215', 'PE02PIC2216D', 'PE02PIC2217', 
                    'PE02PIC2281', 'PE02PIC2282', 'PE02SP1132', 'PE02SP2131', 'PE02SP2132', 'PE02TI2211', 
                    'PE02TI2213', 'PE02TI2214', 'PE02TI2217', 'PE02TI2233B', 
                    'PE02TI2236', 'PE02TI2256', 'PE02TIC2238', 'PE02TIC2258', 'PE02TIC2231B', 'PE02LI2231', 
                    'PE02LI2251', 'PE02LI2261', 'PE02LI2271', 'PE02LI2281', 'PE02LIC2221', 'PE02LIC2232', 
                    'PE02LIC2241', 'PE02LIC2252', 'PE02LIC2261', 'PE02LIC2271',  
                    'PE02WI2411A',  'PE02XI2311', 'PE02SI2311', 'PE02SI2440', 'PE02II2440'], axis = 1)


## Graph 그리기 - 빠른 load를 위해 매 시간 데이터만 추출하였음 ##
ts_plot_n(df_01, 'PE02LI2231')

   
## DELETE 'time' TO APPLY MOVING AVERAGE #
df_02 = df_01.drop(['time'], axis = 1)

## MAKE WHAT HAS NEGATIVE VALUES TO ZERO #

for col in df_02.columns:
    df_02[col][df_02[col] < 0.0001] = 0

    

#### 02. MAKE MOVING AVERAGED DATA SET : 60 min. MOVING AVERAGE #

df_02_ma = df_02.rolling(15).mean()

## ADD 'time' column to MA data set ###
df_ma_15 = pd.concat([df_01['time'], df_02_ma], axis = 1)
#df_cma_15 = pd.concat([df_01['time'], df_02_cma], axis = 1)  # Cumulative Moving Average

del(df_02)

## DELETE Duplicates & NA's #
df_ma_15 = df_ma_15.drop_duplicates('time', keep = 'first')
df_ma_15 = df_ma_15.dropna(axis = 0, how = 'any')

## CHANGE THE TYPE OF 'time' DATA : from object to datetime64
df_ma_15['time'] = pd.to_datetime(df_ma_15['time'])

## SAVE THE FILE ##
df_ma_15.to_csv("C:/GC_POLYMER_2/data_final/data_ma_15_1min_201221.csv")


# SAMPLE 60 MIN. INTERVAL BECAUSE APPLYING 'MERGE" MAKES MEMORY ERROR #
data_60m_interval = df_ma_15.resample(rule = str('60T'),on = 'time').first() # df should be datetime
data_60m_interval.reset_index(drop = True, inplace = True) # DELETE index ('time')

data_60m_interval.head()



####################################################################################################
"""                            LIMS DATA PRE-PROCESSING                                          """
####################################################################################################

#### 03. OPEN LIMS DATA SET - SET UP 'TIME DELAY' : 2015-01-01 ~ 2020-08-31 ####

#-*-coding:utf-8 -*- 
lims_00 = pd.read_csv('C:/GC_POLYMER_2/data_lims/lims_20201217.csv', engine='python')

lims_01 = lims_00[(lims_00.test_type == 'Melt Index_2.16kg_g/10 min')] 
lims_01['grade'] = lims_01['grade'].apply(lambda x: x.split(' ')[1])
lims_01 = lims_01.loc[:, ['time', 'result', 'grade']]
lims_01.dtypes
lims_01['time'] = pd.to_datetime(lims_01['time'])

# CONFIRM & DELETE 'NA' VALUES    
lims_01.info()
lims_01 = lims_01.dropna(axis = 0, how = 'any')



#### 04. BUILD A 3.0 hrs.-TIME LAG DATA SET ######################################################

lims_01['time_2'] = pd.DatetimeIndex(lims_01['time']) - timedelta(hours = 3.0)
lims_02 = lims_01.loc[:, ['time_2', 'result', 'grade']]
#lims_01.rename(columns = {'time_2' : 'time'}, inplace = True)
lims_02.columns = ['time', 'mi', 'grade']

lims_02.describe()
lims_02.info()
lims_02.isnull().sum()
data_60m_interval.isnull().sum()


## INTEGRATE RTDB DATA TO LIMS DATA ##

df_0 = pd.merge(lims_02, data_60m_interval, on = 'time')
df_0.to_csv('C:/GC_POLYMER_2/data_final/POL_final_60MA_MI_20201221_02.csv')

##### THE END OF DATA EXTRACTION ################################################################






























#################################################################################################
####################### POLYMER HDPE 'MI' PREDICTIVE MODELING : 2021-01-21 ######################
#################################################################################################

import os
import pandas as pd 
import numpy as np 
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime, timedelta, date
import time

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.linear_model import LinearRegression, Lasso, LassoCV, ElasticNet, ElasticNetCV
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor 
import xgboost as xgb
import math


def NaNRemove(data):
    for i in range(len(list(data.columns))):
        data = data.dropna(subset=[data.columns[i]], how='any')
    data.index = range(len(data.index))
    return data

def MAPE(y, pred):
    return np.mean(np.abs((y-pred)/y)*100)

""" Historam : Select df, start_Col_num #, end_Col_num, & fraction """
def hist_plot(data, st_col_num, end_col_num, fraction=0.05, bin_num=30):
    s = data.iloc[:, st_col_num:(end_col_num+1)]
    n = s.shape[1]
    plt.figure(figsize=(n*3, 3))
    for i in range(st_col_num-st_col_num, end_col_num-st_col_num+1) :
        temp = s.iloc[:, i].sample(frac=fraction)
        plt.subplot(1, n, (i+1))
        
        plt.title(s.columns[i])
        plt.hist(temp, bins=bin_num)
        plt.subplots_adjust(bottom=0.1, wspace=0.4, hspace=0.4)
    return plt.show()

#hist_plot(df_0, 3, 8)

""" Time-series graph using column number """
def ts_plot(data, col_num): # Time-series graph using column number
    data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S')
    d_ = data[(data['time'].dt.minute==0) & 
              (data['time'].dt.second==0)] #Because of memory, filtered "hourly data"
    iqr = d_.iloc[:, col_num].quantile(0.75) - d_.iloc[:, col_num].quantile(0.25)
    plt.figure(figsize=(10, 4))
    plt.style.use('default')
    plt.title(d_.columns[col_num], fontsize=14)
    plt.scatter(d_['time'], d_.iloc[:, col_num], s=1, color = 'dodgerblue', alpha = 0.5)
    axes = plt.gca()
    axes.yaxis.grid()  
    return plt.show()

""" Time-series graph using column name """
def ts_plot_n(data, col_name): # Time-series graph using column name
    data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S')
    d_ = data[(data['time'].dt.minute==0) & 
              (data['time'].dt.second==0)] #Because of memory, filtered "hourly data"
    plt.figure(figsize=(10, 4))
    plt.style.use('default')
    plt.title(col_name, fontsize=14)
    plt.scatter(d_['time'], d_[col_name], s=1, color = 'brown', alpha = 0.5)
#    plt.ylim([0, 1])
#    plt.xlim(['2018-01-01', '2018-03-30'])
    axes = plt.gca()
    axes.yaxis.grid()  
    return plt.show()

""" Time-series graph using column name & modify y-axis (y_min, y_max) """
def ts_plot_n2(data, col_name, y_min, y_max): # Time-series graph using column name
    data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S')
    d_ = data[(data['time'].dt.minute==0) & 
              (data['time'].dt.second==0)] #Because of memory, filtered "hourly data"
    plt.figure(figsize=(10, 4))
    plt.style.use('default')
    plt.title(col_name, fontsize=14)
    plt.scatter(d_['time'], d_[col_name], s=1, color = 'brown', alpha = 0.5)
    plt.ylim([y_min, y_max])
#    plt.xlim(['2018-01-01', '2018-03-30'])
    axes = plt.gca()
    axes.yaxis.grid()  
    return plt.show()


""" 학습 및 테스트 데이터 구분, 필요없는 데이터 삭제, 데이터 표준화 적용 후 train_y, test_y, train_Xn, test_Xn 값 반환
    Parameters : 전체 데이터명 (data_0), Target변수명, 지워야 하는 변수명 ('time', 'mi', 'grade'):개수 무제한, 
    Train/Test비율, Normalizaion방법(0:Standard, 1:MinMax, 2:Robust) """
def prep_data(df_name, target, scale_x, *args, test_ratio=0.2, norm_num=0) : # args 는 지워야 할 변수명 (time, mi, grade 등)
    X = df_name
    y = df_name[target]
    X_train, X_test, train_y, test_y = train_test_split(X, y, test_size = test_ratio, random_state = 12345)
    train_x = X_train
    test_x = X_test
    for i in range(len(args)):
        train_x = train_x.drop([args[i]], axis = 1)
        test_x = test_x.drop([args[i]], axis = 1)
    if norm_num == 1:
        scalerX = MinMaxScaler()
    elif norm_num == 2:
        scalerX = RobustScaler()
    else :
        scalerX = StandardScaler()
    scalerX.fit(scale_x)
    train_Xn = scalerX.transform(train_x)
    test_Xn = scalerX.transform(test_x)    
    return train_Xn, train_y, test_Xn, test_y, X_test

""" Apply test data & get model performance after Modeling process """
def pred_result(model_name, train_x, train_y, test_x, test_y):
    model_name.fit(train_x, train_y)
    predict_0 = model_name.predict(test_x)
    print("=====================")
    print('RMSE_Model :', format(mean_squared_error(test_y, predict_0)**0.5, ".4f"))
    print('MAPE_Model :', format(MAPE(test_y, predict_0), ".2f"), '(%)')
    print("=====================")    
    return predict_0
    
""" Return RMSE & MAPE for specific model : pred can be one of "predict_0 ~ predict_4" """
def prt_MAPE(test_y, pred):
    print("=====================")
    print('RMSE_Model :', format(mean_squared_error(test_y, pred)**0.5, ".4f"))
    print('MAPE_Model :', format(MAPE(test_y, pred), ".2f"), '(%)')
    print("=====================")
    

""" Draw performance graph : 'Actual' vs 'Predictive' """
def result_plot(x1, y_act, y_pred, point1=0, point2=200, width=12, height=5):
    z0 = pd.DataFrame(x1['time'])
    z0 = z0.reset_index(drop = True)
    z1 = pd.DataFrame(y_act)
    z1 = z1.reset_index(drop = True)
    z2 = pd.DataFrame(y_pred)
    result = pd.concat([z0, z1, z2], axis = 1)
    result.columns = ['time', 'Actual', 'Predictive']
    result = result.sort_values(by = ['time'], axis = 0, ascending = True)
    result = result.set_index('time')
    ## Graphs ##
    plt.style.use('seaborn-whitegrid')
    plt.figure(figsize = (width, height)) 
    plt.plot(result.iloc[point1:point2, 0], color = 'steelblue', alpha = 0.5, markersize = 4.5, 
             marker = 'o', linewidth = 0.5)
    plt.plot(result.iloc[point1:point2, 1], color = 'darkorange', alpha = 0.3, markersize = 4.0, 
             marker = 'o', linewidth = 0.5)
    plt.title('Actual(blue) vs. Predictive(orange)')
    plt.show()
    
    
""" Grid Search for xgboost : Changed 'gamma' & 'learning_rate' only """
def grid_search_xgb(train_x, train_y, test_x, test_y):
    param={'gamma':[.00001, .0001, .001, .01, .1], 'learning_rate':[.001, .01, .1, .5]}
    table = pd.DataFrame()
    rmse_1 = 100 
    mape_1 = 100
    for i in range(len(param['gamma'])):
        for j in range(len(param['learning_rate'])):
            model = xgb.XGBRegressor(n_estimators = 800,
                           gamma = param['gamma'][i], 
                           learning_rate = param['learning_rate'][j], 
                           eta = 0.4,
                           subsample = 0.75,
                           colsample_bytree = 0.5, 
                           max_depth = 8,
                           booster='gbtree')
            pred_2 = model.fit(train_x, train_y)
            predict_0 = model.predict(test_x)
            rmse = mean_squared_error(test_y, predict_0)**0.5
            mape = MAPE(test_y, predict_0)
            table_0 = pd.DataFrame({'gamma':param['gamma'][i], 'learning_rate':param['learning_rate'][j], 'RMSE':[rmse], 'MAPE':[mape]})
            table = table.append(table_0) 
            if rmse <= rmse_1: 
                rmse_1 = rmse
                gamma_best_r = param['gamma'][i]
                l_r_best_r = param['learning_rate'][j]
            if mape <= mape_1: 
                mape_1 = mape
                gamma_best_m = param['gamma'][i]
                l_r_best_m = param['learning_rate'][j]
        print('gamma = ', i+1, '/', len(param['gamma']))   
    
    print('='*59)
    pd.options.display.float_format = '{:.4f}'.format     
    print('Min_RMSE =', format(rmse_1, ".5f"), '/', 'gamma :', gamma_best_r, '/', 'learn_rate :', l_r_best_r)
    print('Min_MAPE =', format(mape_1,".4f"), ' /', 'gamma :', gamma_best_m, '/', 'learn_rate :', l_r_best_m)
    print('n_estimators : 800', '/', 'eta : 0.4', '/', 'subsample : 0.75')
    print('colsample_bytree : 0.5', '/', 'max_depth : 8', '/', 'booster : "gbtree"')
    print('='*59)   
    return table

#val_data=data_valid; train_data=data; target='mi'; args=('time', 'mi', 'grade')
    

def scale_init(df_init, target, *args, test_ratio=0.2, norm_num=0) : # args 는 지워야 할 변수명 (time, mi, grade 등)
    X = df_init
    y = df_init[target]
    X_train, X_test, train_y, test_y = train_test_split(X, y, test_size = test_ratio, random_state = 12345)
    train_x = X_train
    for i in range(len(args)):
        train_x = train_x.drop([args[i]], axis = 1)
    return train_x



def prep_valid(val_data, target, train_x, *args, norm_num=0) : # args 는 지워야 할 변수명 (time, mi, grade 등)
    test_x = val_data
    test_y = val_data[target]

    for i in range(len(args)):
        test_x = test_x.drop([args[i]], axis = 1)
    if norm_num == 1:
        scalerX = MinMaxScaler()
    elif norm_num == 2:
        scalerX = RobustScaler()
    else :
        scalerX = StandardScaler()
    scalerX.fit(train_x)
    train_Xn = scalerX.transform(train_x)
    test_Xn = scalerX.transform(test_x)
    return train_Xn, test_Xn, test_y, val_data

#d_val = prep_valid(data_valid, data, 'mi', 'time', 'mi', 'grade', test_ratio=0.2, norm_num=0)

#d_0 = prep_data(data, 'mi', d_0[0], 'time', 'mi', 'grade') 

""" Display option for the size of rows & columns """
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)


## Set Working Directory ##
os.chdir('C:/GC_POLYMER_2')




#### 01. OPEN DATA SET & DATA PROCESSING #####################################################

df_00 = pd.read_csv('C:/GC_POLYMER_2/data_final/POL_final_60MA_MI_20201221_02.csv')
df_00 = df_00.drop("Unnamed: 0", axis = 1)
df_00['time'] = pd.to_datetime(df_00['time'])

## ADD TAGS : 'PE02FIC_E', 'PE02FIC_PR_2201', 'PE02FIC_PR_2221', 'PE02FIC_PZ', 'PE02FIC_AT',  
df_00.insert(136, 'PE02FIC_E', (df_00['PE02FIC2215A'] + df_00['PE02FIC2215D']))
df_00.insert(137, 'PE02FIC_PR_2201', (df_00['PE02FIC2216A'] + df_00['PE02FIC2216A']))
df_00.insert(138, 'PE02FIC_PR_2221', (df_00['PE02FIC2216D'] + df_00['PE02FIC2216E']))
df_00.insert(139, 'PE02FIC_PZ', (df_00['PE02FIC2112'] + df_00['PE02FIC2113']))
df_00.insert(140, 'PE02FIC_AT', (df_00['PE02FIC2123'] + df_00['PE02FIC2124']))

## SELECT DATA ONLY FOR SERIES MODE ##

seri = (['2500', '2500M', '2520', '2550', '2600D', '2600S', '2600Y', 
         '2610', '3301', '6100', '6610', '7300', '7301', '7302', 
         '8300', '8700', '8700K', '8800', '8800S', '8800U', '8810', '8820'])
df_0 = pd.DataFrame()
for i in range(len(seri)):
    df_1 = df_00[(df_00['grade'] == seri[i])]
    df_0 = pd.concat([df_0, df_1])
del(df_1, seri, i)

df_0 = df_0.sort_values(['time'])


### CONFIRM OUTLIERS : df_0 ##
""" hist_plot(df_0, 8, 12, 1, 50) 
    ts_plot_n(df_0, 'PE02AI2221A1') # > 40 """

df_0 = df_0[(df_0.PE02AI2221A1 > 40) & 
            (df_0.PE02AI2221A2 < 40) & 
            (df_0.PE02AI2221B1 < 40) & 
            (df_0.PE02AIC2243 < 20) &
            (df_0.PE02FIC2113 < 40) & 
            (df_0.PE02FIC2124 < 38) & 
            (df_0.PE02FIC2216B < 40)]




#### 02. MODELING : PREDICTIVE MODEL FOR PRODUCT 'MI' ####################################### 

## Extract recent 3 years data set ###

#data_train = df_0[(df_0.time >= '2017-09-01 00:00:00') & (df_0.time < '2020-09-01 00:00:00')] 
#data_valid = df_0[(df_0.time >= '2020-09-01 00:00:00')] 
data_train = df_0[(df_0.time >= '2017-01-01 00:00:00') & (df_0.time < '2020-11-15 00:00:00')] 
data_valid = df_0[(df_0.time >= '2020-11-15 00:00:00')] 


## 2nd Case : Selected 22 Tags ##
"""
tags_all = (['time', 'mi', 'grade', 'PE02AI2221A1', 'PE02AI2221A2', 'PE02AI2221B1', 'PE02AI2221B2', 
             'PE02AIC2223', 'PE02AIC2243', 'PE02FIC2112', 'PE02FIC2113', 'PE02FIC2123', 'PE02FIC2124', 
             'PE02FIC2215A', 'PE02FIC2215D','PE02FIC2216A', 'PE02FIC2216B', 'PE02FIC2216D', 'PE02FIC2216E', 
             'PE02PIC2231', 'PE02PIC2251', 'PE02TI2234', 'PE02TI2237', 'PE02TI2254', 'PE02TI2257',
             'PE02FIC_E', 'PE02FIC_PR_2201', 'PE02FIC_PR_2221', 'PE02FIC_PZ', 'PE02FIC_AT'])
data_tags = data_train[tags_all] """

###########################################

## Normalization 을  위해 전체 범위 데이터의 train_x 데이터를 기준으로 Scaler 설정
data = data_train
## Set the 'base scalerX' of entire Modeling: scale_init(df_name, target, *args, test_ratio=0.2, norm_num=0)
scale_x = scale_init(data, 'mi', 'time', 'mi', 'grade', test_ratio=0.2, norm_num=0)



## Model 0) Model for entire range of 'MI' ####################################
data = data_train
## Set the 'base scalerX' of entire Modeling: scale_init(df_name, target, *args, test_ratio=0.2, norm_num=0)
#scale_x = scale_init(data, 'mi', 'time', 'mi', 'grade', test_ratio=0.2, norm_num=0)

#data = data_tags
# Prepare data set for modeling : prep_data(df_name, target, scaler_x, *args, test_ratio=0.2, norm_num=0)
d_0 = prep_data(data, 'mi', scale_x, 'time', 'mi', 'grade') 
# Grid Search for xgboost : 'gamma' & 'learning_rate' are varied - (train_x, train_y, test_x, test_y):
# Return a Table(opt_gamma) in terms of  gamma, learning_rate, RMSE, MAPE
#opt_gamma = grid_search_xgb(d_0[0], d_0[1], d_0[2], d_0[3])

## MODELING BY USE OF XGB ALGORITHM ##
model_00 = xgb.XGBRegressor(n_estimators = 800, 
                           gamma = 0.0001,
                           learning_rate = 0.1, 
                           eta = 0.4,
                           subsample = 0.75,
                           colsample_bytree = 0.5, 
                           max_depth = 8,
                           booster='gbtree')
# Modeling Result : pred_result(model_name, train_x, train_y, test_x, test_y)
pred_0 = pred_result(model_00, d_0[0], d_0[1], d_0[2], d_0[3])

# Plotting : result_plot(x1, y_act, y_pred, point1=0, point2=200, width=12, height=5)
#result_plot(d_0[4], d_0[3], pred_0) 

## Assign Model_0 : (train_x, train_y)
model_00 = model_00.fit(d_0[0], d_0[1]) 

""" 
===========================================================
Min_RMSE = 0.04522 / gamma : 1e-05 / learn_rate : 0.1
Min_MAPE = 6.8151  / gamma : 0.0001 / learn_rate : 0.1
n_estimators : 800 / eta : 0.4 / subsample : 0.75
colsample_bytree : 0.5 / max_depth : 8 / booster : "gbtree"
=========================================================== """



## Model 1) Model for MI < 0.055 ##############################################
p1 = 0.0
p2 = 0.055
data = data_train[(data_train.mi > p1) & (data_train.mi < p2)] 

# Prepare data set for modeling : prep_data(df_name, target, scaler_x, *args, test_ratio=0.2, norm_num=0)
d_1 = prep_data(data, 'mi', scale_x, 'time', 'mi', 'grade') 
#opt_gamma = grid_search_xgb(d_1[0], d_1[1], d_1[2], d_1[3])

model_01 = xgb.XGBRegressor(n_estimators = 800, 
                           gamma = 0.00001,
                           learning_rate = 0.1, 
                           eta = 0.4,
                           subsample = 0.75,
                           colsample_bytree = 0.5, 
                           max_depth = 8,
                           booster='gbtree')
pred_1 = pred_result(model_01, d_1[0], d_1[1], d_1[2], d_1[3])
#result_plot(d_1[4], d_1[3], pred_1) 

model_01 = model_01.fit(d_1[0], d_1[1]) 

"""
data = df_0[(df_0.mi < 0.055)]
=======================================================
Min_RMSE = 0.00166 | gamma : 1e-05 | learn_rate : 0.1
Min_MAPE = 2.4377  | gamma : 1e-05 | learn_rate : 0.1
=======================================================

data = data_train[(data_train.mi < 0.055)] 
=====================
RMSE_Model : 0.0015
MAPE_Model : 2.30 (%)
===================== """

## Model 2) Model for 0.055 <= MI < 0.65 ##############################################
p1 = 0.04
p2 = 0.12

data = data_train[(data_train.mi > p1) & (data_train.mi <= p2)] 

d_2 = prep_data(data, 'mi', scale_x, 'time', 'mi', 'grade') 
#opt_gamma = grid_search_xgb(d_2[0], d_2[1], d_2[2], d_2[3])


model_02 = xgb.XGBRegressor(n_estimators = 1500, 
                           gamma = 0.000005,
                           learning_rate = 0.01, 
                           eta = 0.4,
                           subsample = 0.85,
                           colsample_bytree = 0.5, 
                           max_depth = 8,
                           booster='gbtree')
pred_2 = pred_result(model_02, d_2[0], d_2[1], d_2[2], d_2[3])
#result_plot(d_2[4], d_2[3], pred_2) 

model_02 = model_02.fit(d_2[0], d_2[1]) 

"""
data = data_train[(data_train.mi >= 0.04) & (data_train.mi < 0.12)]
===========================================================
Min_RMSE = 0.00307 / gamma : 1e-05 / learn_rate : 0.01
Min_MAPE = 3.1144  / gamma : 1e-05 / learn_rate : 0.01
n_estimators : 800 / eta : 0.4 / subsample : 0.75
colsample_bytree : 0.5 / max_depth : 8 / booster : "gbtree"
===========================================================

gamma = 0.000005, learning_rate = 0.01
===========================================================
RMSE_Model : 0.0030
MAPE_Model : 2.97 (%)
n_estimators : 1500 / eta : 0.4 / subsample : 0.85
colsample_bytree : 0.5 / max_depth : 8 / booster : "gbtree"
========================================================== """



## Model 3) Model for 0.1 <= MI < 0.22 ##############################################
p1 = 0.1
p2 = 0.22
data = data_train[(data_train.mi > p1) & (data_train.mi <= p2)] 

#ts_plot_n2(data, 'mi', p1, p2) # Time-series graph using column name

d_3 = prep_data(data, 'mi', scale_x, 'time', 'mi', 'grade') 
#opt_gamma = grid_search_xgb(d_3[0], d_3[1], d_3[2], d_3[3])


model_03 = xgb.XGBRegressor(n_estimators = 1200, 
                           gamma = 0.000001,
                           learning_rate = 0.01, 
                           eta = 0.4,
                           subsample = 0.75,
                           colsample_bytree = 0.5, 
                           max_depth = 8,
                           booster='gbtree')
pred_3 = pred_result(model_03, d_3[0], d_3[1], d_3[2], d_3[3])

#result_plot(d_3[4], d_3[3], pred_3) 
model_03 = model_03.fit(d_3[0], d_3[1]) 

"""
===========================================================
Min_RMSE = 0.01263 / gamma : 1e-05 / learn_rate : 0.01
Min_MAPE = 4.5509  / gamma : 1e-05 / learn_rate : 0.01
n_estimators : 800 / eta : 0.4 / subsample : 0.75
colsample_bytree : 0.5 / max_depth : 8 / booster : "gbtree"
===========================================================

gamma = 0.000001, learning_rate = 0.01,
===========================================================
RMSE_Model : 0.0125
MAPE_Model : 4.43 (%)
n_estimators : 1200 / eta : 0.4 / subsample : 0.75
colsample_bytree : 0.5 / max_depth : 8 / booster : "gbtree"
===========================================================
"""

## Model 04. PREDICTIVE MODEL FOR Model for 0.15 <= MI < 0.20 ######################
p1 = 0.15
p2 = 0.20

data = data_train[(data_train.mi > p1) & (data_train.mi <= p2)] 

d_4 = prep_data(data, 'mi', scale_x, 'time', 'mi', 'grade') 
#opt_gamma = grid_search_xgb(d_4[0], d_4[1], d_4[2], d_4[3])

model_04 = xgb.XGBRegressor(n_estimators = 1500, 
                           gamma = 0.00005,
                           learning_rate = 0.01, 
                           eta = 0.4,
                           subsample = 0.75,
                           colsample_bytree = 0.7, 
                           max_depth = 8,
                           booster='gbtree')
pred_4 = pred_result(model_04, d_4[0], d_4[1], d_4[2], d_4[3])
#result_plot(d_4[4], d_4[3], pred_4) 

model_04 = model_04.fit(d_4[0], d_4[1]) 

"""
gamma = 0.00005, learning_rate = 0.01
===========================================================
RMSE_Model : 0.0079
MAPE_Model : 3.50 (%)
n_estimators : 1800 / eta : 0.4 / subsample : 0.75
colsample_bytree : 0.7 / max_depth : 8 / booster : "gbtree"
===========================================================
"""


## Model 05. PREDICTIVE MODEL FOR Model for 0.3 <= MI < 0.4 ######################
p1 = 0.3
p2 = 0.4

data = data_train[(data_train.mi > p1) & (data_train.mi <= p2)] 
#ts_plot_n2(data, 'mi', p1, p2) # Time-series graph using column name

d_5 = prep_data(data, 'mi', scale_x, 'time', 'mi', 'grade') 
#opt_gamma = grid_search_xgb(d_5[0], d_5[1], d_5[2], d_5[3])

model_05 = xgb.XGBRegressor(n_estimators = 800, 
                           gamma = 0.001,
                           learning_rate = 0.1, 
                           eta = 0.4,
                           subsample = 0.75,
                           colsample_bytree = 0.5, # 0.6 is the best
                           max_depth = 6,
                           booster='gbtree')
pred_5 = pred_result(model_05, d_5[0], d_5[1], d_5[2], d_5[3])

#result_plot(d_5[4], d_5[3], pred_5) 
model_05 = model_05.fit(d_5[0], d_5[1]) 

"""
gamma = 0.0001, learning_rate = 0.1
===========================================================
RMSE_Model : 0.0186
MAPE_Model : 3.83 (%)
n_estimators : 800 / eta : 0.4 / subsample : 0.75
colsample_bytree : 0.5 / max_depth : 8 / booster : "gbtree"
===========================================================
"""


## Model 06. PREDICTIVE MODEL FOR Model for 0.25 <= MI < 0.4 ########################
p1 = 0.25
p2 = 0.4
data = data_train[(data_train.mi > p1) & (data_train.mi <= p2)] 

#ts_plot_n2(data, 'mi', p1, p2) # Time-series graph using column name

d_6 = prep_data(data, 'mi', scale_x, 'time', 'mi', 'grade') 
#opt_gamma = grid_search_xgb(d_6[0], d_6[1], d_6[2], d_6[3])

model_06 = xgb.XGBRegressor(n_estimators = 1800, 
                           gamma = 0.00001,
                           learning_rate = 0.01, 
                           eta = 0.4,
                           subsample = 0.9,
                           colsample_bytree = 0.75, 
                           max_depth = 8,
                           booster='gbtree')
pred_6 = pred_result(model_06, d_6[0], d_6[1], d_6[2], d_6[3])
#result_plot(d_6[4], d_6[3], pred_6) 

model_06 = model_06.fit(d_6[0], d_6[1]) 

"""
===========================================================
Min_RMSE = 0.01848 / gamma : 0.0001 / learn_rate : 0.01
Min_MAPE = 4.1236  / gamma : 0.0001 / learn_rate : 0.01
n_estimators : 800 / eta : 0.4 / subsample : 0.75
colsample_bytree : 0.5 / max_depth : 8 / booster : "gbtree"
=========================================================== 

gamma = 0.00001, learning_rate = 0.01
===========================================================
RMSE_Model : 0.0177
MAPE_Model : 4.02 (%)
n_estimators : 1800 / eta : 0.4 / subsample : 0.9
colsample_bytree : 0.75 / max_depth : 8 / booster : "gbtree"
===========================================================

"""

## Model 07. PREDICTIVE MODEL FOR Model for 0.45 <= MI < 1.15 #################
p1 = 0.45
p2 = 1.15
data = data_train[(data_train.mi > p1) & (data_train.mi <= p2)] 
#ts_plot_n2(data, 'mi', p1, p2) # Time-series graph using column name

d_7 = prep_data(data, 'mi', scale_x, 'time', 'mi', 'grade') 
#opt_gamma = grid_search_xgb(d_7[0], d_7[1], d_7[2], d_7[3])

model_07 = xgb.XGBRegressor(n_estimators = 1800, 
                           gamma = 0.01,
                           learning_rate = 0.01, 
                           eta = 0.4,
                           subsample = 0.85,
                           colsample_bytree = 0.5, 
                           max_depth = 5,
                           booster='gbtree')
pred_7 = pred_result(model_07, d_7[0], d_7[1], d_7[2], d_7[3])

#result_plot(d_7[4], d_7[3], pred_7) 
model_07 = model_07.fit(d_7[0], d_7[1]) 

"""
===========================================================
Min_RMSE = 0.08578 / gamma : 0.1 / learn_rate : 0.01
Min_MAPE = 7.1494  / gamma : 0.01 / learn_rate : 0.01
n_estimators : 800 / eta : 0.4 / subsample : 0.75
colsample_bytree : 0.5 / max_depth : 8 / booster : "gbtree"
===========================================================

gamma = 0.01, learning_rate = 0.01,
===========================================================
RMSE_Model : 0.0850
MAPE_Model : 6.89 (%)
n_estimators : 1800 / eta : 0.4 / subsample : 0.85
colsample_bytree : 0.5 / max_depth : 5 / booster : "gbtree"
===========================================================
"""

## Model 08. PREDICTIVE MODEL FOR 0.75 < MI ##############################################
p1 = 0.75
p2 = data_train.mi.max()
data = data_train[(data_train.mi > p1) & (data_train.mi <= p2)] 

#ts_plot_n2(data, 'mi', p1, p2) # Time-series graph using column name

d_8 = prep_data(data, 'mi', scale_x, 'time', 'mi', 'grade') 
#opt_gamma = grid_search_xgb(d_8[0], d_8[1], d_8[2], d_8[3])

model_08 = xgb.XGBRegressor(n_estimators = 800, 
                           gamma = 0.0001,
                           learning_rate = 0.01, 
                           eta = 0.4,
                           subsample = 0.9,
                           colsample_bytree = 0.2, 
                           max_depth = 9,
                           booster='gbtree')
pred_8 = pred_result(model_08, d_8[0], d_8[1], d_8[2], d_8[3])
#result_plot(d_8[4], d_8[3], pred_8) 

model_08 = model_08.fit(d_8[0], d_8[1]) 

"""
gamma = 0.0001, learning_rate = 0.01
===========================================================
RMSE_Model : 0.0553
MAPE_Model : 4.09 (%)
n_estimators : 800 / eta : 0.4 / subsample : 0.75
colsample_bytree : 0.5 / max_depth : 8 / booster : "gbtree"
=========================================================== """



## Model 09. PREDICTIVE MODEL FOR 1.0 < MI ##############################################
p1 = 1.0
p2 = data_train.mi.max()
data = data_train[(data_train.mi > p1) & (data_train.mi <= p2)] 

d_9 = prep_data(data, 'mi', scale_x, 'time', 'mi', 'grade')  
#opt_gamma = grid_search_xgb(d_9[0], d_9[1], d_9[2], d_9[3])

model_09 = xgb.XGBRegressor(n_estimators = 800, 
                           gamma = 0.0001,
                           learning_rate = 0.1, 
                           eta = 0.4,
                           subsample = 0.75,
                           colsample_bytree = 0.75, 
                           max_depth = 6,
                           booster='gbtree')
pred_9 = pred_result(model_09, d_9[0], d_9[1], d_9[2], d_9[3])
#result_plot(d_9[4], d_9[3], pred_9) 

model_09 = model_09.fit(d_9[0], d_9[1]) 

"""
gamma = 0.0001, learning_rate = 0.1
=======================================================
RMSE_Model : 0.0561
MAPE_Model : 3.03 (%)
n_estimators : 800 / eta : 0.4 / subsample : 0.75
colsample_bytree : 0.75 / max_depth : 6 / booster : "gbtree"
=======================================================
"""



########### VALIDATE MODEL : 2021-01-25 #######################################################
## Validate the model using "data_valid" set

""" 'mi' range for each model

Model #      MI coverage            MAPE for Train model
model_00 : 0 < MI < 2.5             6.81
model_01 : 0 < MI < 0.055           2.30
model_02 : 0.04 < MI <= 0.12        2.97
model_03 : 0.1 < MI < 0.22          4.43
model_04 : 0.15 < MI < 0.2          3.50
model_05 : 0.25 < MI < 0.4          4.02
model_06 : 0.3 < MI < 0.4           3.83
model_07 : 0.45 < MI < 0.75         6.89
model_08 : 0.75 <= MI               4.09
model_09 : 1.0 < MI                 3.03
"""

d_val = prep_valid(data_valid, 'mi', scale_x, 'time', 'mi', 'grade')

mi_pred = list()
pred_model_00 = []

for i in range(len(d_val[1])) :
    test_data = d_val[1][i]
    test_data_0 = test_data.reshape(1,-1)  # row & col. transpose
    predict_000 = model_00.predict(test_data_0)
    
    if predict_000 <= 0.055 :
        predict_val = model_02.predict(test_data_0)
#        print(predict_val)
        
    elif predict_000 > 0.055 and predict_000 <= 0.12 :
        predict_val = (model_01.predict(test_data_0) + model_02.predict(test_data_0))/2
#        print(predict_val)
        
    elif predict_000 > 0.12 and predict_000 <= 0.4 :
        predict_val = (model_03.predict(test_data_0) + model_04.predict(test_data_0) + 
                                + model_05.predict(test_data_0))/3
#        print(predict_val)
        
    elif predict_000 > 0.4 and predict_000 <= 0.75 :
        predict_val = (model_07.predict(test_data_0) + model_06.predict(test_data_0))/2
#        print(predict_val)
        
    else : 
        predict_val = (model_08.predict(test_data_0) + model_09.predict(test_data_0) + predict_000)/3
#        print(predict_val)
    
#    predict_val = [predict_val]
    mi_pred = np.append(mi_pred, predict_val)
    pred_model_00 += [predict_000]

mi_pred_0 = pd.DataFrame(mi_pred)    
mi_pred_0.columns = ['predictive']
pred_model_00 = pd.DataFrame(pred_model_00)    
pred_model_00.columns = ['pred_model_00']
val_y = pd.DataFrame(d_val[3].iloc[:, 1].reset_index(drop = True))
aaa = pd.concat([val_y, pred_model_00, mi_pred_0], axis = 1)


print('RMSE_Mod_00 :', format(mean_squared_error(aaa['mi'], aaa['pred_model_00'])**0.5, ".4f"))
print('MAPE_Mod_00 :', format(MAPE(aaa['mi'], aaa['pred_model_00']), ".2f"), '(%)')
print('RMSE_Mod_new :', format(mean_squared_error(aaa['mi'], aaa['predictive'])**0.5, ".4f"))
print('MAPE_Mod_new :', format(MAPE(aaa['mi'], aaa['predictive']), ".2f"), '(%)')





