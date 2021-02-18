from flask import Flask, jsonify, request, render_template,request,url_for
from flask_cors import CORS

from flask_uploads import UploadSet,configure_uploads,IMAGES,DATA,ALL
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine, MetaData, text, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from collections import OrderedDict

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

# Python API
# from model import *

# configuration
DEBUG = True

# Base
Base = declarative_base()

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

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
engine = create_engine('mysql+mysqldb://root:root@localhost/newdatabase',echo = True)
Session = sessionmaker(bind=engine)
session = Session()

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
		file = request.files['csv_data']
		# dataInfo 테이블 생성
		Base.metadata.create_all(engine)
		# pandas
		df = pd.read_csv(file)
		df = df.reset_index().rename(columns={"index": "ID"})
		
		table_name = 'dataset'
		# csv to sql
		df.to_sql (
			table_name,
			engine,
			if_exists='replace',
			index=False,
			chunksize=500,
			method='multi'
		)  
	# return jsonify(df.to_dict())
		return summarizeData(df)

@app.route('/addData',methods=['GET','POST'])
def addData():
	response_object = {'status': 'success'}
	post_data = request.json
	# .to_sql를 사용하기 위해서 dict 데이터를 dataframe으로 변환함
	dictToDf = pd.DataFrame(post_data, index=[0])
	# 변환한 dataframe을 to_sql을 사용해서 mysql에 append함
	table_name = 'dataset'
	dictToDf.to_sql (
				table_name,
				engine,
				if_exists='append',
				index=False,
				chunksize=200,
				method='multi'
			)
	response_object['message'] = 'Data added!'
   # sql을 .read_sql_table로 읽어들이고 frontend에 return 해줌
	return jsonify(response_object)

@app.route('/loadData',methods=['GET','POST'])
def loadData():
	data = pd.read_sql_table('dataset', session.bind)
	# print(data)
	session.close()
	return jsonify(data.to_dict())

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

@app.route('/dataSummarize',methods=['GET','POST'])
def dataSummarize():
  df = pd.read_csv('./static/uploadsDB/iris.csv')
  return (summarizeData(df))

if __name__ == '__main__':
    app.run(debug=True)