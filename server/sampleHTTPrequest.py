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
            'No':2979, 
            'SiteName':"Jeju",
            'DATE':"2021-07-01 15:00:00.097",
            'AIDATA1':0,
            'AIDATA2':0,
            'AIDATA3':0,
            'AIDATA4':0,
            'AIDATA5':0,
            'AIDATA6':0,
            'AIDATA7':0,
            'AIDATA8':0,
            'AIDATA9':0,
            'AIDATA10':0
        }
        # 롯데에서 메일로 보내준 형식이랑 맞는지 확인
    jsonarraydata = {}
    jsonarraydata['con'] = json.dumps(jsoncondata) #con항목에 AI 데이터 대입
    jsonarraydata['cnf'] = 'json'
    jsonarraydata['lbl'] = 10

    bodydata = {}
    bodydata['m2m:cin'] = jsonarraydata

    print(str(json.dumps(bodydata))) #Body Data값 정의

    res = requests.post(serverURL,
    json.dumps(bodydata),headers=headers) #data 빼고

    print("\nResponse Platfrom : " + res.text + '\n')
    return res.text

if __name__ =="__main__":
    serverURL ="http://124.243.30.77/~/biogas/base/SlottencBioGas-S00030064_BIOGAS/AIDatalogs"
    requestHTTP(serverURL)








# # 제주 조회
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
#     serverURL =" http://124.243.30.77/~/biogas/base/SlottencBioGas-S00030064_BIOGAS/logs/la"
#     requestHTTP(serverURL)