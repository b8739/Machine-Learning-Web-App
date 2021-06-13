#-*- coding:utf-8 -*-
import requests #HTTP 요청을 보내기 위한 라이브러리
import json

# 제주 등록
def requestHTTP(serverURL):

    #header 파일
    headers = {     
        'Accept' : 'application/json',
        'X-M2M-Origin' : '/SlottencBioGas-S00030064_BIOGAS',
        'X-M2M-RI' : '{{$timestamp}}_{{$randomInt}}',
        'Content-Type' : 'application/vnd.onem2m-res+json;ty=4',
        'Authorization' : 'Bearer 229c9ec1-1f55-405b-a1a7-9d3034e140e3'
                }

    jsoncondata = {
        'No':1, #받아와서
        'SiteName':"제주",#받아와서
        'Date':"2021-06-09 14:31:19.103",#받아와서 
        'AIDATA1':1,
        'AIDATA2':2,
        'AIDATA3':3,
        'AIDATA4':4,
        'AIDATA5':5,
        'AIDATA6':6,
        'AIDATA7':7,
        'AIDATA8':8,
        'AIDATA9':9,
        'AIDATA10':10
        } #AI 데이터
    # 롯데에서 메일로 보내준 형식이랑 맞는지 확인
    jsonarraydata = {}
    jsonarraydata['cnf'] = 'json'
    jsonarraydata['lbl'] = 10
    jsonarraydata['con'] = json.dumps(jsoncondata) #con항목에 AI 데이터 대입

    bodydata = {}
    bodydata['m2m:cin'] = jsonarraydata

    print(headers) # 헤더값 정의
    print(str(json.dumps(bodydata))) #Body Data값 정의

    res = requests.post(serverURL,data=json.dumps(bodydata),headers=headers)

    print("\nResponse Platfrom : " + res.text + '\n')
    return res.text

if __name__ =="__main__":
    serverURL ="http://124.243.30.77/~/biogas/base/SlottencBioGas-S00030064_BIOGAS/AIDatalogs"
    requestHTTP(serverURL)

# 제주 조회
# def requestHTTP(serverURL):

#     #header 파일
#     # Authorization = 'Bearer 6865803b-842f-4757-98e2-27d8687bddff' #Deivce Key값.
#     headers = {     
#         'Accept' : 'application/json',
#         'X-M2M-Origin' : '/SlottencBioGas-S00030064_BIOGAS',
#         'X-M2M-RI' : '{{$timestamp}}_{{$randomInt}}',
#         'Authorization' : 'Bearer 229c9ec1-1f55-405b-a1a7-9d3034e140e3'
#     }

#     res = requests.get(serverURL,headers=headers)

#     print("\nResponse Platfrom : " + res.text + '\n')
#     return res.text

# if __name__ =="__main__":
#     serverURL ="http://124.243.30.77/~/biogas/base/SlottencBioGas-S00030064_BIOGAS/logs/la"
#     requestHTTP(serverURL)