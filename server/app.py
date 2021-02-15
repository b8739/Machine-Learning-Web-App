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

# newData=Dataset(sepal_width=5)

session = Session()
# session.add(newData)
# session.commit()


 
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
	conn = engine.connect()
	data = pd.read_sql_table('dataset', conn)
	# print(data)
	conn.close()
	return jsonify(data.to_dict())

@app.route('/updateData', methods=['PUT', 'DELETE'])
def updateData():
	# if request.method == 'PUT':
	# 	put_data = request.get_json
		# dictToDf = pd.DataFrame(put_data, index=[0])
		# print(dictToDf)
		# 임시 update방법, 근데 query를 안 사용할 순 없을까?
		# print(put_data)
		# print(request.get_json)
		# print(request.json)
		# conn = engine.connect()
		# num = put_data['index']
		# print(num)
		# df = pd.read_sql_query("select * from dataset limit "+num+",1;", conn)
		# for key, value in put_data.items()
		# 	setattr(df,key,value)
		# conn.close
		# print(df)
		# --
# if request.method == 'DELETE':
	return jsonify("uploader")


if __name__ == '__main__':
    app.run(debug=True)