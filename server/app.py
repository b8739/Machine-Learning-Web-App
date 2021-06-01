
# flask
from flask import Flask, jsonify, request, render_template,request,url_for, Response
from flask_cors import CORS
from flask_uploads import UploadSet,configure_uploads,IMAGES,DATA,ALL


# sqlalchemy
from sqlalchemy import create_engine, MetaData, text, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from flask_mysqldb import MySQL

from config import DB_URL

from werkzeug.utils  import secure_filename
import os
import sys
sys.path.append('/Users/jeongjaeho/attic_project/mlApp/server/modeling')
import datetime
import time
import json

# EDA Packages
import pandas as pd 
import numpy as np 

from dataSummarizer import summarizeData
from xgboost_modeling import *
from svr_modeling import *
from rf_modeling import *


# pyarrow
import pyarrow as pa
from pyarrow import csv

# Python API
# from model import *

# configuration
DEBUG = True

# Base
Base = declarative_base()

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = False

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# 임시 schema
class DataInfo(Base):
    __tablename__ = 'dataInfo'
    columnName = Column(String(300),primary_key=True)
    dataType = Column(String(300))
    normalization = Column(String(300))
    mean = Column(Integer)
    stdev = Column(String(300))
    quartile = Column(String(300))
    numofna = Column(String(300))
    
# engine_dataset
URI_dataset = 'mysql+mysqldb://root:0000@localhost/newdatabase'
URI_modeling = 'mysql+mysqldb://root:0000@localhost/modeling'
engine_dataset = create_engine(URI_dataset,echo = False)
engine_modeling = create_engine(URI_modeling,echo = False)
Session = sessionmaker(bind=engine_dataset,autocommit=False)
session = Session()


# autocommit = 0 (false)
# sql = "SET AUTOCOMMIT = 0;"
# session.execute(sql)

# john = DataInfo(columnName = '2')
# session.add(john)

# # Commit the new User John to the database
# session.commit()


@app.route('/', methods=['GET'])
def testing():
	return jsonify ("hello world")

# Route for our Processing and Details Page
@app.route('/dataupload',methods=['GET','POST'])
def dataupload():
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()

  if request.method == 'POST' and 'csv_data' in request.files:
    # 테이블 이름 받아오기
    tableName = request.args.get('tableName')
  

    file = request.files['csv_data']
	# dataInfo 테이블 생성
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
    sql = "drop table if exists temp_dataset;"
    session.execute(sql)

    sql = "create table temp_dataset as select * from dataset;"
    session.execute(sql)
    session.commit()
    session.close

  # method='multi'
  # traditional한 sql에선 method multi를 하면 더 느려진다고 함
  
	# return jsonify(df.to_dict())
    return summarizeData(df)

""" 
addData: Dataset에 data를 'Add'할 때 라우팅
"""

@app.route('/addData',methods=['GET','POST'])
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

@app.route('/loadData',methods=['GET','POST'])
def loadData():
    Session = sessionmaker(bind=engine_dataset,autocommit=False)
    session = Session()
  ### 1) 데이터를 SQL에 저장하고 해당 SQL을 TABLE로 불러오던 기존 방식 ###
    data = pd.read_sql_table('temp_dataset', session.bind)
    # return jsonify(data.to_dict())
    return Response(data.to_json(), mimetype='application/json') #json array로 반환됨

  # ### 2) CSV 파일을 읽어서 DICT 형태로 RETURN해주는 방식 (1번 방식이 속도가 느려서 일단 2번으로 진행) ###
  # df = pd.read_csv('./static/uploadsDB/all_stocks_2017-01-01_to_2018-01-01.csv')
  # return jsonify(df.to_dict())



@app.route('/updateData', methods=['PUT', 'DELETE'])
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
@app.route('/infiniteLoading',methods=['GET','POST'])
def infiniteLoading():
	limit = request.args.get('limit')
	conn = engine_dataset.connect()
	df = pd.read_sql_query("select * from temp_dataset limit "+limit+",45;", conn)
	conn.close
	return Response(df.to_json( orient='records'), mimetype='application/json')


@app.route('/dataSummarize',methods=['GET','POST'])
def dataSummarize():
  df = pd.read_csv('./static/uploadsDB/all_stocks_2017-01-01_to_2018-01-01.csv')
  return (summarizeData(df))

@app.route('/deleteColumn',methods=['GET'])
def deleteColumn():
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()
  columnToDelete = request.args.get('columnToDelete')
  sql = "alter table temp_dataset drop column "+ columnToDelete+";"
  session.execute(sql)
#   session.commit()
  session.close()
  return jsonify ("hello world")

@app.route('/overwriteTable',methods=['GET'])
def overwriteTable():
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()
  sql = "drop table dataset"
  session.execute(sql)
    
  sql = "rename table temp_dataset to dataset"
  session.execute(sql)

  sql = "create table temp_dataset as select * from dataset;"
  session.execute(sql)
  
  session.commit()
  session.close()
  return jsonify ("overwrited")

@app.route('/duplicateTable',methods=['GET'])
def duplicateTable():
  newTableName = request.args.get('newTableName')
  sql = "create table "+newTableName+" as select * from temp_dataset;"
  session.execute(sql)
  session.commit()
  session.close()
  return jsonify ("duplicateTable")

@app.route('/deleteRow',methods=['GET'])
def deleteRow():
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()

  timeSeriesCondition = request.args.get('timeSeriesCondition')
  featureConditions = request.args.getlist('featureConditions[]')
  sql = "delete from temp_dataset where"
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

@app.route('/deleteRowByPeriod',methods=['GET'])
def deleteRowByPeriod():
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()

  getFullTimeSeries_from = request.args.get('getFullTimeSeries_from')
  getFullTimeSeries_to = request.args.get('getFullTimeSeries_to')

#  query
  
  getFirstIndexQuery="select ID from temp_dataset where ts like '%"+getFullTimeSeries_from+"%' limit 1;"
  startIndex =  str(session.execute(getFirstIndexQuery).fetchall()[0][0])
  # print(startIndex)

  getEndIndexQuery="select ID from temp_dataset where ts like '%"+getFullTimeSeries_to+"%' order by id DESC LIMIT 1;"
  endIndex =  str(session.execute(getEndIndexQuery).fetchall()[0][0])


  deleteRowByIndexQuery="delete from temp_dataset where ID >= " +startIndex+ " && ID <= "+endIndex  
  session.execute(deleteRowByIndexQuery)

  session.commit()
  session.close()

  return jsonify (getFullTimeSeries_from)

@app.route('/showTables',methods=['GET'])
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

@app.route('/changeColumnName',methods=['GET'])
def changeColumnName():
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()

  newName = request.args.get('columnName')
  columnIndex = str(int(request.args.get('columnIndex'))+1)
  # sql
  getOriginalNameQuery="select column_name from information_schema.columns where table_name = 'temp_dataset' and ordinal_position = "+columnIndex
  originalName = session.execute(getOriginalNameQuery).fetchall()[0][0]
  
  getOriginalTypeQuery="select data_type from information_schema.columns where table_name = 'temp_dataset' and column_name = '"+originalName+"'"
  originalType=session.execute(getOriginalTypeQuery).fetchall()[0][0]

  changeNameQuery = 'ALTER TABLE temp_dataset CHANGE '+ originalName +' '+ newName+' '+originalType

  session.execute(changeNameQuery)
  session.commit()
  session.close()
  return jsonify(newName)

@app.route('/changeColumnOrder',methods=['GET'])
def changeColumnOrder():
  Session = sessionmaker(bind=engine_dataset,autocommit=False)
  session = Session()
  position = request.args.get('position')
  movedColumnName = request.args.get('movedColumnName')
  newIndex = request.args.get('newIndex')

  # get original name
  getOriginalNameQuery="select column_name from information_schema.columns where table_name = 'temp_dataset' and ordinal_position = "+newIndex
  originalName=session.execute(getOriginalNameQuery).fetchall()[0][0]
  # get original type
  getOriginalTypeQuery="select data_type from information_schema.columns where table_name = 'temp_dataset' and column_name = '"+originalName+"'"
  originalType=session.execute(getOriginalTypeQuery).fetchall()[0][0]
  # position (right/left)에 따라서 구분
  if (position == 'left'):
    sql = "ALTER TABLE temp_dataset MODIFY COLUMN " +movedColumnName+ ' ' +originalType+ ' BEFORE '+ originalName
  elif (position == 'right'):
    sql = "ALTER TABLE temp_dataset MODIFY COLUMN " +movedColumnName+ ' ' +originalType+ ' AFTER '+ originalName
  session.execute(sql)
  session.commit()
  session.close()
  return jsonify('hello')

@app.route('/loadSummarizedData',methods=['GET'])
def loadSummarizedData():
  df = pd.read_sql_table('temp_dataset', session.bind)

  return (summarizeData(df))

@app.route('/xgboost_modeling',methods=['GET'])
def xgboost_modeling():
  modelingOption_str = request.args.get('modelingOption')
  print(modelingOption_str)
  modelingOption_list = modelingOption_str.split(',')
  # 개발 편의성 속성 직접 받지 않고 주석처리
  # for index,value in enumerate(modelingOption_list):
  #   # 문자에 .이 포함되어있으면 소수이니 float으로 변환
  #   if modelingOption_list[index].find('.') != -1:
  #     modelingOption_list[index] = float(value)
  #   # 아니라면 (.이 포함되어 있지 않으면) 정수이니 int로 변환
  #   else: 
  #     modelingOption_list[index] = int(value)
  print(modelingOption_list)
  return (xgboost(modelingOption_list))

@app.route('/svr_modeling',methods=['GET'])
def svr_modeling():
  modelingOption_str = request.args.get('modelingOption')

  modelingOption_list = modelingOption_str.split(',')
  print(modelingOption_list)
  # 개발 편의상 주석처리
  # for index,value in enumerate(modelingOption_list):
  #   #str이 아닐 때 (int/float일 때)만 if 문 작동
  #   print(modelingOption_list[index].isalpha()==False)
  #   if modelingOption_list[index].isalpha()==False:
  #     # 문자에 .이 포함되어있으면 소수이니 float으로 변환
  #     if modelingOption_list[index].find('.') != -1:
  #       modelingOption_list[index] = float(value)
  #     # 아니라면 (.이 포함되어 있지 않으면) 정수이니 int로 변환
  #     else: 
  #       modelingOption_list[index] = int(value)
  print(modelingOption_list)
  return (svr(modelingOption_list))

@app.route('/rf_modeling',methods=['GET'])
def rf_modeling():
  modelingOption_str = request.args.get('modelingOption')
  print(modelingOption_str)
  modelingOption_list = modelingOption_str.split(',')

  for index,value in enumerate(modelingOption_list):
    # 문자에 .이 포함되어있으면 소수이니 float으로 변환
    if modelingOption_list[index].find('.') != -1:
      modelingOption_list[index] = float(value)
    # 아니라면 (.이 포함되어 있지 않으면) 정수이니 int로 변환
    else: 
      modelingOption_list[index] = int(value)
  print(modelingOption_list)
  return (rf(modelingOption_list))

@app.route('/saveModel',methods=['POST'])
def saveModel():
  # get request data
  caseName = request.get_json()['caseName']

  # make case_list table
  Session = sessionmaker(bind=engine_modeling,autocommit=False)
  session = Session()

  sql = "CREATE TABLE case_list (case_name char(20), PRIMARY KEY(case_name));"
  session.execute(sql)

  sql = " insert into case_list (case_name) VALUE ('"+caseName+"');"
  session.execute(sql)
  session.commit()
  session.close
  """ 
  1) modelingOption 전처리 및 테이블 삽입
  """
  # convert (json -> df)
  modelingOption = [1,2,3,4,5,6,7]
  modelingOption_dict = {'n_estimators':'','learning_rate':'','gamma':'','eta':'','subsample':'','colsample_bytree':'','max_depth':''}
  index = 0 
  for key in modelingOption_dict:
    modelingOption_dict[key] = modelingOption[index]
    index += 1
  modelingOption_df = pd.DataFrame(modelingOption_dict,index=[caseName])

  # name tables (test & valid)
  tableName_modelingOption = caseName + '_parameter'
  
  # convert (df -> sql)
  modelingOption_df.to_sql (
    tableName_modelingOption,
    engine_modeling,
    if_exists='replace',
    index=False,
    chunksize=10000,
  ) 
  """ 
  2) modelingSummary 전처리 및 테이블 삽입
  """
  # convert 'modelingSummary' (json -> df)
  modelingSummary = request.get_json()['modelingSummary']
  modelingSummary = json.loads(modelingSummary)
  modelingSummary_test_df = pd.DataFrame(modelingSummary['test'],index=[caseName])
  modelingSummary_valid_df = pd.DataFrame(modelingSummary['valid'],index=[caseName])
  
  # name tables (test & valid)
  tableName_modelingSummary_test = caseName + '_test'
  tableName_modelingSummary_valid = caseName + '_valid'

  # convert (df -> sql)
  modelingSummary_test_df.to_sql (
    tableName_modelingSummary_test,
    engine_modeling,
    if_exists='replace',
    index=False,
    chunksize=10000,
  )
  modelingSummary_valid_df.to_sql (
    tableName_modelingSummary_valid,
    engine_modeling,
    if_exists='replace',
    index=False,
    chunksize=10000,
  )  
  return jsonify('hello')

@app.route('/loadCases',methods=['GET'])
def loadCases():
  Session = sessionmaker(bind=engine_modeling,autocommit=False)
  session = Session()

  sql="select * from case_list"
  caseRow = session.execute(sql).fetchall()
  print(caseRow[0][0])
  caseList = []
  for index,case in enumerate(caseRow):
    caseList.append(str(caseRow[index][0]))
  return jsonify(caseList)

if __name__ == '__main__':
    app.run(debug=True)