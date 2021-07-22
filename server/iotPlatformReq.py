#-*- coding:utf-8 -*-
import requests #HTTP 요청을 보내기 위한 라이브러리
import json
# time
from datetime import datetime
import time

import numpy as np
from random import *
'''
l  제주 조회 URL : http://124.243.30.77/~/biogas/base/SlottencBioGas-S00030064_BIOGAS/logs/la
l  제주 전송 URL : http://124.243.30.77/~/biogas/base/SlottencBioGas-S00030064_BIOGAS/AIDatalogs
l  제주 헤더 값 X-M2M-Origin:  /SlottencBioGas-S00030064_BIOGAS
l  제주 헤더 값 Authorization : Bearer 229c9ec1-1f55-405b-a1a7-9d3034e140e3
l  이천 조회 URL : http://124.243.30.77/~/biogas/base/SlottencBioGas-S0003031_ICHEONBIO/logs/la
l  이천 전송 URL : http://124.243.30.77/~/biogas/base/SlottencBioGas-S0003031_ICHEONBIO/AIDatalogs
l  이천 헤더 값 X-M2M-Origin:  /SlottencBioGas-S0003031_ICHEONBIO
l  이천 헤더 값 Authorization : Bearer 6865803b-842f-4757-98e2-27d8687bddff
'''

# 제주 전송
def requestHTTP(serverURL):
    currentDatetime = str(datetime.fromtimestamp(time.time()))

    #header 파일
    headers = {     
        'Accept' : 'application/json',
        'X-M2M-Origin' : '/SlottencBioGas-S00030064_BIOGAS',  #제주 헤더
        'X-M2M-RI' : '{{$timestamp}}_{{$randomInt}}', #제주 헤더
        'Content-Type' : 'application/vnd.onem2m-res+json;ty=4', #제주 헤더
        'Authorization' : 'Bearer 229c9ec1-1f55-405b-a1a7-9d3034e140e3' #제주 헤더
                }

    jsoncondata = {
            'No':10, 
            'SiteName':"제주",
            'DATE':currentDatetime, #현재시간으로 해야함
            'AIDATA1':6,
            'AIDATA2':2,
            'AIDATA3':1,
            'AIDATA4':6,
            'AIDATA5':3,
            'AIDATA6':8,
            'AIDATA7':6,
            'AIDATA8':1,
            'AIDATA9':7,
            'AIDATA10':9
            }

    jsonarraydata = {}
    jsonarraydata['con'] = json.dumps(jsoncondata,ensure_ascii = False) #con항목에 AI 데이터 대입
    jsonarraydata['cnf'] = 'json'
    jsonarraydata['lbl'] = 10

    bodydata = {}
    bodydata['m2m:cin'] = jsonarraydata

    print(str(json.dumps(bodydata,ensure_ascii = False))) #Body Data값 정의

    res = requests.post(serverURL,
    json.dumps(bodydata),headers=headers) 

    print("\nResponse Platfrom : " + res.text + '\n')
    return res.text

if __name__ =="__main__":
    serverURL ="http://124.243.30.77/~/biogas/base/SlottencBioGas-S00030064_BIOGAS/AIDatalogs" #제주 전송
    requestHTTP(serverURL)

