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
import datetime
import time

# EDA Packages
import pandas as pd 
import numpy as np 

from dataSummarizer import summarizeData

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
    
# engine
engine = create_engine('mysql+mysqldb://root:0000@localhost/newdatabase',echo = False)
Session = sessionmaker(bind=engine,autocommit=False)
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
  if request.method == 'POST' and 'csv_data' in request.files:
    # 테이블 이름 받아오기
    tableName = request.args.get('tableName')
    print(tableName)

    file = request.files['csv_data']
	# dataInfo 테이블 생성
    Base.metadata.create_all(engine)
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
			engine,
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
				engine,
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
  ### 1) 데이터를 SQL에 저장하고 해당 SQL을 TABLE로 불러오던 기존 방식 ###
    data = pd.read_sql_table('temp_dataset', session.bind)
    # return jsonify(data.to_dict())
    return Response(data.to_json(), mimetype='application/json') #json array로 반환됨

  # ### 2) CSV 파일을 읽어서 DICT 형태로 RETURN해주는 방식 (1번 방식이 속도가 느려서 일단 2번으로 진행) ###
  # df = pd.read_csv('./static/uploadsDB/all_stocks_2017-01-01_to_2018-01-01.csv')
  # return jsonify(df.to_dict())

@app.route('/duplicateTable',methods=['GET','POST'])
def duplicateTable():
  #테이블 복제


  return jsonify("hello")

""" 
updateData: Dataset의 data을 수정할때의 라우팅
"""

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
	conn = engine.connect()
	df = pd.read_sql_query("select * from temp_dataset limit "+limit+",45;", conn)
	conn.close
	return Response(df.to_json( orient='records'), mimetype='application/json')


@app.route('/dataSummarize',methods=['GET','POST'])
def dataSummarize():
  df = pd.read_csv('./static/uploadsDB/all_stocks_2017-01-01_to_2018-01-01.csv')
  return (summarizeData(df))

@app.route('/deleteColumn',methods=['GET'])
def deleteColumn():
  columnToDelete = request.args.get('columnToDelete')
  sql = "alter table temp_dataset drop column "+ columnToDelete+";"
  session.execute(sql)
#   session.commit()
  session.close()
  return jsonify ("hello world")

@app.route('/saveTable',methods=['GET'])
def saveTable():
  saveOption = request.args.get('saveOption')
  print (saveOption)

  if saveOption == 'overwrite':
    sql = "drop table dataset"
    session.execute(sql)
    
    sql = "rename table temp_dataset to dataset"
    session.execute(sql)

    sql = "create table temp_dataset as select * from dataset;"
    session.execute(sql)

#     sql = "truncate table dataset"
#     session.execute(sql)
#     sql = "create table dataset (select * from temp_dataset)"
#     session.execute(sql)

#   elif saveOption == 'newDataset':
#     sql = 'Create Table newDataset ( select * from dataset );'
#     session.execute(sql)
  
  session.commit()
  session.close()
  return jsonify ("overwrited")

@app.route('/deleteRowByDate',methods=['GET'])
def deleteRow():
  timeSeriesText = request.args.get('timeSeriesText')
  sql = "delete from temp_dataset where ts like '%"+timeSeriesText+"%';"
  session.execute(sql)
  session.commit()
  session.close()
  print (sql)
  return jsonify (timeSeriesText)

@app.route('/deleteRowByPeriod',methods=['GET'])
def deleteRowByPeriod():

  getFullTimeSeries_from = request.args.get('getFullTimeSeries_from')
  getFullTimeSeries_to = request.args.get('getFullTimeSeries_to')

#  query
  
  getFirstIndexQuery="select ID from temp_dataset where ts like '%"+getFullTimeSeries_from+"%' limit 1;"
  startIndex =  str(session.execute(getFirstIndexQuery).fetchall()[0][0])
  # print(startIndex)

  getEndIndexQuery="select ID from temp_dataset where ts like '%"+getFullTimeSeries_to+"%' order by id DESC LIMIT 1;"
  endIndex =  str(session.execute(getEndIndexQuery).fetchall()[0][0])
  print(endIndex)

  deleteRowByIndexQuery="delete from temp_dataset where ID >= " +startIndex+ " && ID <= "+endIndex  
  session.execute(deleteRowByIndexQuery)

  session.commit()
  session.close()

  return jsonify (getFullTimeSeries_from)

@app.route('/showTables',methods=['GET'])
def showTables():
  sql="show tables;"
  tableList=[]
  tableInfo = list(session.execute(sql).fetchall())
  for index,tableName in enumerate(tableInfo):
    tableList.append(str(tableName[0]))
  print(tableList)
  session.commit()
  session.close()
  return jsonify(tableList)

if __name__ == '__main__':
    app.run(debug=True)