from flask import Flask, jsonify, request, render_template,request,url_for
from flask_cors import CORS

from flask_uploads import UploadSet,configure_uploads,IMAGES,DATA,ALL
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine, MetaData, text, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from flask_mysqldb import MySQL

from config import DB_URL

from werkzeug.utils  import secure_filename
import os
import datetime
import time

# EDA Packages
import pandas as pd 
import numpy as np 

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
# class Dataset(Base):
#     __tablename__ = 'dataset'
#     sepal_length = Column(Integer,primary_key=True)
#     sepal_width = Column(Integer)
#     petal_length = Column(Integer)
#     petal_width = Column(Integer)
#     species = Column(String(300))
    
# engine
engine = create_engine('mysql+mysqldb://root:root@localhost/newdatabase',echo = True)
Session = sessionmaker(bind=engine)
session = Session()
# newData=Dataset(sepal_width=5)


# session.add(newData)
# session.commit()

# 임시 update방법, 근데 query를 안 사용할 순 없을까?
# __tablename__ = "dataset"
# columnName = 'sepal_length'
# index = '0'
# sql = "UPDATE"+__tablename__+"SET"+columnName+"='2002 WHERE index = "+index+";"


@app.route('/', methods=['GET'])
def testing():
	return jsonify ("hello world")

# Route for our Processing and Details Page
@app.route('/dataupload',methods=['GET','POST'])
def dataupload():
	if request.method == 'POST' and 'csv_data' in request.files:
		file = request.files['csv_data']

		# pandas
		dataset_df = pd.read_csv(file)
		dataset_df = dataset_df.reset_index().rename(columns={"index": "ID"})
		table_name = 'dataset'
		# csv to sql
		dataset_df.to_sql (
			table_name,
			engine,
			if_exists='replace',
			index=False,
			chunksize=500,
			method='multi'
		)  
	return jsonify(dataset_df.to_dict())

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


if __name__ == '__main__':
    app.run(debug=True)