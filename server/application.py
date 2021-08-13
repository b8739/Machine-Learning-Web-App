
# flask
from flask import Flask, jsonify, request, render_template,request,url_for, Response, send_from_directory

from flask_cors import CORS
from flask_uploads import UploadSet,configure_uploads,IMAGES,DATA,ALL


# sqlalchemy
from sqlalchemy.sql.sqltypes import VARCHAR
from sqlalchemy import create_engine, MetaData, text, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from flask_mysqldb import MySQL

from config import *

from werkzeug.utils  import secure_filename
import os
import sys
sys.path.append('./modeling')
sys.path.append('./simulation')
import datetime
import time
import json

# EDA Packages
import pandas as pd 
import numpy as np 

# summarizer
from dataSummarizer import summarizeData
from normalDistribution import randGenerator_nd

# modeling
from xgboost_modeling import *
from svr_modeling import *
from rf_modeling import *

# simulation
from simulation import getSimulationResult


# pyarrow
import pyarrow as pa
from pyarrow import csv

# collections
from collections import OrderedDict, defaultdict

# Python API
# from model import *

# configuration
DEBUG = True

    
# engine_dataset (로컬용)
# URI_dataset = 'mysql+mysqldb://root:0000@localhost/datasets'
# URI_modeling = 'mysql+mysqldb://root:0000@localhost/project_1'
# engine_dataset = create_engine(URI_dataset,echo = False)
# engine_modeling = create_engine(URI_modeling,echo = False)
# Session = sessionmaker(bind=engine_dataset,autocommit=False)
# session = Session()

# engine_dataset (개발용)
engine_dataset = create_engine(datasets_URL,echo = False)
engine_modeling = create_engine(modeling_URL,echo = False)
Session = sessionmaker(bind=engine_dataset,autocommit=False)
session = Session()

# autocommit = 0 (false)
# sql = "SET AUTOCOMMIT = 0;"
# session.execute(sql)


# @application.route('/')
# def index():
#   # changed to send_static_file
#   return application.send_static_file('index.html')

# Base
Base = declarative_base()

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(ROOT_PATH, 'dist')
STATIC_URL_PATH = os.path.join(STATIC_PATH, 'static')

# instantiate the app

application = Flask(__name__, static_folder=STATIC_PATH,static_url_path='', template_folder=STATIC_PATH)
application.config.from_object(__name__)
application.config["TEMPLATES_AUTO_RELOAD"] = False

# enable CORS
CORS(application, resources={r'/*': {'origins': '*'}})

# route
@application.route('/', defaults={'path': ''})
@application.route('/<string:path>')
def index(path):

  # return render_template('index.html')
  # return application.send_static_file('index.html')
  return send_from_directory(STATIC_PATH,'index.html')



# Route for our Processing and Details Page
@application.route('/dataupload',methods=['GET','POST'])
def dataupload():
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()

  if request.method == 'POST' and 'csv_data' in request.files:
    # 테이블 이름 받아오기
    tableName = request.args.get('tableName')
  

    file = request.files['csv_data']
	# dataset 테이블 생성
    Base.metadata.create_all(engine_dataset)
    # pyarrow
    pyarrow_table = csv.read_csv(file)
    df = pyarrow_table.to_pandas()
    # df = pd.read_csv(file)
		# pandas
    # df = pd.read_csv(file, dtype={"ts": "category"})
    # df = pd.concat(tp)
    df = df.reset_index().rename(columns={"index": "ID"})
		# csv to sql
    df.to_sql (
			tableName,
			engine_dataset,
			if_exists='replace',
			index=False,
			chunksize=10000,
		) 
    # duplicate table
    # sql = "drop table if exists dataset;"
    # session.execute(sql)

    # sql = "create table dataset as select * from dataset;"
    # session.execute(sql)
    # session.commit()
    # session.close

  # method='multi'
  # traditional한 sql에선 method multi를 하면 더 느려진다고 함
  
	# return jsonify(df.to_dict())
    return summarizeData(df)

""" 
addData: Dataset에 data를 'Add'할 때 라우팅
"""

@application.route('/addData',methods=['GET','POST'])
def addData():
	response_object = {'status': 'success'}
	post_data = request.json
	# .to_sql를 사용하기 위해서 dict 데이터를 dataframe으로 변환함
	dictToDf = pd.DataFrame(post_data, index=[0])
	# 변환한 dataframe을 to_sql을 사용해서 mysql에 append함
	tableName = 'dataset'
	dictToDf.to_sql (
				tableName,
				engine_dataset,
				if_exists='append',
				index=False,
				chunksize=4000,
				method='multi',
				keep_default_na=False
			)
	response_object['message'] = 'Data added!'
   # sql을 .read_sql_table로 읽어들이고 frontend에 return 해줌
	return jsonify(response_object)



""" 
loadData: Frontend에서 Dataset을 로드해오는 라우팅
"""

@application.route('/loadData',methods=['GET','POST'])
def loadData():
    Session = sessionmaker(bind=engine_dataset,autocommit=False)
    session = Session()
  ### 1) 데이터를 SQL에 저장하고 해당 SQL을 TABLE로 불러오던 기존 방식 ###

    data = pd.read_sql_table('dataset', session.bind)
    del data["ID"]
    print (data)
    data = data.to_dict(orient='records',into=OrderedDict)
    # return jsonify(data.to_dict())
    # return Response(data, mimetype='application/json') #json object로 반환됨 (data.csv 정상작동, 허나 컬럼별 object)
    # print(data.to_dict(orient='records',into=OrderedDict))
    return json.dumps(data)
    # return jsonify(data)
    # return Response(json.dumps(data),mimetype='application/json') #boston은 정상적으로 json array 반환 (행별), data.csv는 string이 반환됨

  # ### 2) CSV 파일을 읽어서 DICT 형태로 RETURN해주는 방식 (1번 방식이 속도가 느려서 일단 2번으로 진행) ###
  # df = pd.read_csv('./static/uploadsDB/all_stocks_2017-01-01_to_2018-01-01.csv')
  # return jsonify(df.to_dict())



@application.route('/updateData', methods=['PUT', 'DELETE'])
def updateData():
	if request.method == 'PUT':
		post_data = request.get_json() #json으로 하면 dict is not callable뜸
		index = post_data['ID']
		# SQL문 작성
  
		# sql = "UPDATE dataset SET "+targetColumn+" = " + updatedValue + " WHERE ID = " + targetID+";"

		# session.execute(sql)
		# session.commit()
		# session.close()
  
		# targetColumn 받아오기
		targetColumn = ''
		for key, value in post_data.items():
			if(key!='ID'):
				targetColumn += key + " = " + value + ", "
		targetColumn = targetColumn[:len(targetColumn)-2]

		# sql문 작성
		sql = "UPDATE dataset SET "+targetColumn + " WHERE ID = " + index+";"
		session.execute(sql)
		session.commit()
		session.close()
	return jsonify("hello")

""" 
infinite-loading Test: 
"""
@application.route('/infiniteLoading',methods=['GET','POST'])
def infiniteLoading():
	limit = request.args.get('limit')
	conn = engine_dataset.connect()
	df = pd.read_sql_query("select * from dataset limit "+limit+",45;", conn)
	conn.close
	return Response(df.to_json( orient='records'), mimetype='application/json')


@application.route('/deleteColumn',methods=['GET'])
def deleteColumn():
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()
  columnToDelete = request.args.get('columnToDelete')
  sql = "alter table dataset drop column "+ columnToDelete+";"
  session.execute(sql)
#   session.commit()
  session.close()
  return jsonify ("hello world")

@application.route('/overwriteTable',methods=['GET'])
def overwriteTable():
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()
    ##여기 logic이 들어감
  sql = ""
  session.execute(sql)
    
  
  session.commit()
  session.close()
  return jsonify ("overwrited")

@application.route('/duplicateTable',methods=['GET'])
def duplicateTable():
  newTableName = request.args.get('newTableName')
  sql = "create table "+newTableName+" as select * from dataset;"
  session.execute(sql)
  session.commit()
  session.close()
  return jsonify ("duplicateTable")

@application.route('/deleteRow',methods=['GET'])
def deleteRow():
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()

  timeSeriesCondition = request.args.get('timeSeriesCondition')
  featureConditions = request.args.getlist('featureConditions[]')
  sql = "delete from dataset where"
  if (timeSeriesCondition!=None):
    tsConditionQuery = " ts like '%"+timeSeriesCondition+"%'"
    sql+=tsConditionQuery
  if (featureConditions!=[]):
    for featureCondition in featureConditions:
      featureConditionQuery = ' And '+featureCondition
      sql += featureConditionQuery

  session.execute(sql)
  session.commit()
  session.close()
  return jsonify (sql)

@application.route('/deleteRowByPeriod',methods=['GET'])
def deleteRowByPeriod():
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()

  getFullTimeSeries_from = request.args.get('getFullTimeSeries_from')
  getFullTimeSeries_to = request.args.get('getFullTimeSeries_to')

#  query
  
  getFirstIndexQuery="select ID from dataset where ts like '%"+getFullTimeSeries_from+"%' limit 1;"
  startIndex =  str(session.execute(getFirstIndexQuery).fetchall()[0][0])
  # print(startIndex)

  getEndIndexQuery="select ID from dataset where ts like '%"+getFullTimeSeries_to+"%' order by id DESC LIMIT 1;"
  endIndex =  str(session.execute(getEndIndexQuery).fetchall()[0][0])


  deleteRowByIndexQuery="delete from dataset where ID >= " +startIndex+ " && ID <= "+endIndex  
  session.execute(deleteRowByIndexQuery)

  session.commit()
  session.close()

  return jsonify (getFullTimeSeries_from)

@application.route('/showTables',methods=['GET'])
def showTables():
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()

  sql="show tables;"
  tableList=[]
  tableInfo = list(session.execute(sql).fetchall())
  for index,tableName in enumerate(tableInfo):
    tableList.append(str(tableName[0]))

  session.commit()
  session.close()
  return jsonify(tableList)

@application.route('/changeColumnName',methods=['GET'])
def changeColumnName():
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()

  newName = request.args.get('columnName')
  columnIndex = str(int(request.args.get('columnIndex'))+1)
  # sql
  getOriginalNameQuery="select column_name from information_schema.columns where table_name = 'dataset' and ordinal_position = "+columnIndex
  originalName = session.execute(getOriginalNameQuery).fetchall()[0][0]
  
  getOriginalTypeQuery="select data_type from information_schema.columns where table_name = 'dataset' and column_name = '"+originalName+"'"
  originalType=session.execute(getOriginalTypeQuery).fetchall()[0][0]

  changeNameQuery = 'ALTER TABLE dataset CHANGE '+ originalName +' '+ newName+' '+originalType

  session.execute(changeNameQuery)
  session.commit()
  session.close()
  return jsonify(newName)

@application.route('/changeColumnOrder',methods=['GET'])
def changeColumnOrder():
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()
  position = request.args.get('position')
  movedColumnName = request.args.get('movedColumnName')
  newIndex = request.args.get('newIndex')

  # get original name
  getOriginalNameQuery="select column_name from information_schema.columns where table_name = 'dataset' and ordinal_position = "+newIndex
  originalName=session.execute(getOriginalNameQuery).fetchall()[0][0]
  # get original type
  getOriginalTypeQuery="select data_type from information_schema.columns where table_name = 'dataset' and column_name = '"+originalName+"'"
  originalType=session.execute(getOriginalTypeQuery).fetchall()[0][0]
  # position (right/left)에 따라서 구분
  if (position == 'left'):
    sql = "ALTER TABLE dataset MODIFY COLUMN " +movedColumnName+ ' ' +originalType+ ' BEFORE '+ originalName
  elif (position == 'right'):
    sql = "ALTER TABLE dataset MODIFY COLUMN " +movedColumnName+ ' ' +originalType+ ' AFTER '+ originalName
  session.execute(sql)
  session.commit()
  session.close()
  return jsonify('hello')

@application.route('/loadSummarizedData',methods=['GET'])
def loadSummarizedData():
  df = pd.read_sql_table('dataset', session.bind)
  return (summarizeData(df))

@application.route('/loadRandomInfo',methods=['GET'])
def loadDistributionData():
  # df = pd.read_sql_table('dataset', session.bind)
  return (randGenerator_nd())

@application.route('/xgboost_modeling',methods=['POST'])
def xgboost_modeling():
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()
  ### 1) 데이터를 SQL에 저장하고 해당 SQL을 TABLE로 불러오던 기존 방식 ###
  data = pd.read_sql_table('dataset', session.bind)
  session.close()
  # modeling
  modelingRequest = request.get_json()['modelingRequest']
  splitRatio = request.get_json()['splitRatio']
  print('splitRatio',splitRatio)
  print('modelingRequest',modelingRequest)
  # splitRatio = request.get_json()['splitRatio']

  # modelingOption_list = [1]
  # 개발 편의성 속성 직접 받지 않고 주석처리
  # for index,value in enumerate(modelingOption_list):
  #   # 문자에 .이 포함되어있으면 소수이니 float으로 변환
  #   if modelingOption_list[index].find('.') != -1:
  #     modelingOption_list[index] = float(value)
  #   # 아니라면 (.이 포함되어 있지 않으면) 정수이니 int로 변환
  #   else: 
  #     modelingOption_list[index] = int(value)

  return (xgboost(data,splitRatio,modelingRequest))
  # return jsonify(modelingRequest)

@application.route('/svr_modeling',methods=['POST'])
def svr_modeling():
  # readdata
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()
  ### 1) 데이터를 SQL에 저장하고 해당 SQL을 TABLE로 불러오던 기존 방식 ###
  data = pd.read_sql_table('dataset', session.bind)
  session.close()
  # modeling
  modelingRequest = request.get_json()['modelingRequest']
  splitRatio = request.get_json()['splitRatio']
  print('splitRatio',splitRatio)
  print('modelingRequest',modelingRequest)

  # # 개발 편의상 주석처리
  # for index,value in enumerate(modelingOption_list):
  #   #str이 아닐 때 (int/float일 때)만 if 문 작동
  #   # print(modelingOption_list[index].isalpha()==False)
  #   if modelingOption_list[index].isalpha()==False:
  #     # 문자에 .이 포함되어있으면 소수이니 float으로 변환
  #     if modelingOption_list[index].find('.') != -1:
  #       modelingOption_list[index] = float(value)
  #     # 아니라면 (.이 포함되어 있지 않으면) 정수이니 int로 변환
  #     else: 
  #       modelingOption_list[index] = int(value)

  return (svr(data,splitRatio,modelingRequest))

@application.route('/rf_modeling',methods=['POST'])
def rf_modeling():
  # readdata
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()
  ### 1) 데이터를 SQL에 저장하고 해당 SQL을 TABLE로 불러오던 기존 방식 ###

  data = pd.read_sql_table('dataset', session.bind)
  session.close()
  # modeling
  modelingRequest = request.get_json()['modelingRequest']
  splitRatio = request.get_json()['splitRatio']
  print('splitRatio',splitRatio)
  print('modelingRequest',modelingRequest)

  # for index,value in enumerate(modelingOption_list):
  #   # 문자에 .이 포함되어있으면 소수이니 float으로 변환
  #   if modelingOption_list[index].find('.') != -1:
  #     modelingOption_list[index] = float(value)
  #   # 아니라면 (.이 포함되어 있지 않으면) 정수이니 int로 변환
  #   else: 
  #     modelingOption_list[index] = int(value)
  # return jsonify('hello')
  return (rf(data,splitRatio,modelingRequest))

@application.route('/saveModel',methods=['POST'])
def saveModel():
  """ 
  Request로 받아서 저장해야 할 항목 (한번 저장 시 총 8개 테이블):
  1. Case Name 
    -> case_list ['case_name'], 

  2. algorithm 
    -> case_list ['algorithm'] 

  3. Modeling Parameter 
    -> ['<case이름>_parameter']

  4. Modeling Summary 
    -> ['<case이름>_test/valid_summary']

  5. Modeling Dataset (Actual Predictive) 
    -> ['<case이름>_test/valid_actual/predictive']
  """

  """ Session 생성 (engine_modeling) """
  Session = sessionmaker(bind=engine_modeling,autocommit=False)
  session = Session()

  """ 
  1. Case Name, 
  2. algorithm 저장 
  """

  case_name = request.get_json()['case_name']
  algorithm = request.get_json()['algorithm']

  dict = {'case_name':case_name,'algorithm':algorithm}

  case_name_df = pd.DataFrame(dict,index=[0])
  case_name_df['dataset'] = 'dataset_1'
  
  case_name_df.to_sql (
    'case_list',
    engine_modeling,
    if_exists='append',
    index=False,
    chunksize=10000,
  ) 

  """ 3. Modeling Parameter 저장 """

  # convert (json -> df)
  modelingOption = [1,2,3,4,5,6,7]
  modelingOption_dict = {'n_estimators':'','learning_rate':'','gamma':'','eta':'','subsample':'','colsample_bytree':'','max_depth':''}
  index = 0 
  for key in modelingOption_dict:
    modelingOption_dict[key] = modelingOption[index]
    index += 1
    
  modelingOption_df = pd.DataFrame(modelingOption_dict,index=[case_name])
  modelingOption_df.index.name = 'case_name'
  
  # convert (df -> sql)
  modelingOption_df.to_sql (
    'parameter',
    engine_modeling,
    if_exists='append',
    dtype={"case_name": VARCHAR(10)},
    chunksize=10000,
  ) 
  """  4. Modeling Summary 저장 """
    # convert 'modelingSummary' (json -> df)
  modelingSummary = request.get_json()['modelingSummary']
  modelingSummary = json.loads(modelingSummary)

  modelingSummary_test_df = pd.DataFrame(modelingSummary['test'],index=[case_name])
  modelingSummary_test_df.index.name = 'case_name'
  modelingSummary_test_df['type'] = 'test'

  modelingSummary_valid_df = pd.DataFrame(modelingSummary['valid'],index=[case_name])
  modelingSummary_valid_df.index.name = 'case_name'
  modelingSummary_valid_df['type'] = 'valid'

  modelingSummary_df = pd.concat([modelingSummary_test_df,modelingSummary_valid_df])

  # convert (df -> sql)
  modelingSummary_df.to_sql (
    'summary',
    engine_modeling,
    dtype={"case_name": VARCHAR(10)},
    if_exists='append',
    chunksize=10000,
  )

  """ 5. Modeling Dataset (Actual/Predictive)저장 """

  graphSources = request.get_json()['graphSources']
  graphSources = json.loads(graphSources)

  # 1) df 생성, 2) 컬럼 추가 (case 이름), 3) 컬럼 순서 재설정
  test_df = pd.DataFrame(graphSources['test'])
  test_df['case_name'] = case_name
  test_df = test_df[['case_name', 'Actual', 'Predictive']]

  # df -> sql table
  test_df.to_sql (
    'dataset_test',
    engine_modeling,
    if_exists='append',
    index=False,
    chunksize=10000,
  ) 

  valid_df = pd.DataFrame(graphSources['valid'])
  valid_df['case_name'] = case_name
  valid_df = valid_df[['case_name', 'Actual', 'Predictive']]

  valid_df.to_sql (
    'dataset_valid',
    engine_modeling,
    if_exists='append',
    index=False,
    chunksize=10000,
  )
  session.commit()
  session.close
  return jsonify('hello')

@application.route('/loadCases',methods=['GET'])
def loadCases():
  Session = sessionmaker(bind=engine_modeling,autocommit=False)
  session = Session()

  sql="select * from case_list"
  caseRow = session.execute(sql).fetchall()
  caseDict={'case_name':'','algorithm':'','dataset':''}
  caseList = []
  for index,case in enumerate(caseRow):
    caseDict['case_name']=caseRow[index][0]
    caseDict['algorithm']=caseRow[index][1]
    caseDict['dataset']=caseRow[index][2]
    caseList.append({'case_name':caseDict['case_name'],'algorithm': caseDict['algorithm'],
    'dataset': caseDict['dataset']})
    # caseList.append(str(caseRow[index][0]))
  session.commit()
  session.close
  return jsonify(caseList)

@application.route('/changeCase',methods=['GET'])
def changeCase():
  Session = sessionmaker(bind=engine_modeling,autocommit=False)
  session = Session()

  case_name = request.args.get('case_name')
  """ 1) Graph """
  # sql 정의
  test_actual="select Actual from dataset_test where case_name = '"+case_name +"';"
  test_predictive="select Predictive from dataset_test where case_name = '"+case_name +"';"
  valid_actual="select Actual from dataset_valid where case_name = '"+case_name +"';"
  valid_predictive="select Predictive from dataset_valid where case_name = '"+case_name +"';"

  # sql 실행 반환 값 저장 (test & valid dataset)
  test_actual_list = []
  for i,c in enumerate(session.execute(test_actual).fetchall()):
    test_actual_list.append(c[0])
  
  test_predictive_list = []
  for i,c in enumerate(session.execute(test_predictive).fetchall()):
    test_predictive_list.append(c[0])

  valid_actual_list = []
  for i,c in enumerate(session.execute(valid_actual).fetchall()):
    valid_actual_list.append(c[0])

  valid_predictive_list = []
  for i,c in enumerate(session.execute(valid_predictive).fetchall()):
    valid_predictive_list.append(c[0])

  # return format 정리
  modeling_dataset = {'test':None,'valid':None}
  modeling_dataset['test'] = {'Actual':test_actual_list,'Predictive':test_predictive_list}
  modeling_dataset['valid'] = {'Actual':valid_actual_list,'Predictive':valid_predictive_list}
  
  """ 2) Table """
  caseList = []
  test_modelingSummary = "select * from summary where case_name = '"+case_name +"';"

  listConverted = []
  for i,c in enumerate(session.execute(test_modelingSummary).fetchall()):
    listConverted.append(list(c))
    listConverted[i].pop(0)
    listConverted[i].pop(-1)

  modeling_summary = {'test':{'MAPE':listConverted[0][0],'RMSE':listConverted[0][1],'R_square':listConverted[0][2]},
  'valid':{'MAPE':listConverted[1][0],'RMSE':listConverted[1][1],'R_square':listConverted[1][2]}}

  # print(modeling_summary)

  return jsonify(modeling_dataset,modeling_summary)

@application.route('/loadProjects',methods=['GET'])
def loadProjects():
  Session = sessionmaker(bind=engine_modeling,autocommit=False)
  session = Session()
  sql = "SHOW DATABASES LIKE '%project%';"
  project_list = []
  for i,v in enumerate(session.execute(sql).fetchall()):
    project_list = project_list+list(v)
  # print(project_list)
  session.commit()
  session.close
  return jsonify(project_list)

@application.route('/runSimulation',methods=['POST'])
def runSimulation():
  observedVariable = request.get_json()['observedVariable']
  rangeInfo = request.get_json()['rangeInfo']
  print (rangeInfo)
  return getSimulationResult(observedVariable,rangeInfo)


if __name__ == '__main__':
    application.run()