# from app import df
import pandas as pd 
import numpy as np 
import os
import json

import json
from app import jsonify, Response


def randGenerator_nd(): 

  df_00 = pd.read_csv("boston_house.csv")
  
  df_00_mean = df_00.mean().round(2) #그 외 변수의 mean (평균)
  df_00_std = df_00.std().round(1) #그 외 변수의 std (표준편차)

  df_00_info = pd.DataFrame({'mean':df_00_mean.values,'std':df_00_std.values})
  finalRangeInfo = {}

  for i,v in df_00_info.iterrows():
      mean = v[0]
      std = v[1]

      randomized = np.random.normal(mean,std,10000)

      featureName = df_00.columns[i]

      minValue = min(randomized).round(2)
      maxValue = max(randomized).round(2)

      rangeInfo = {'min':minValue,'max':maxValue}

      finalRangeInfo[featureName]=rangeInfo
  
  return jsonify(finalRangeInfo)
  
