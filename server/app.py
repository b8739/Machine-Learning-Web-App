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

# session = Session()
# session.add(newData)
# session.commit()


@app.route('/', methods=['GET'])
def testing():
	return jsonify('Hello World!')

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
	# addData_df = pd.read_json(post_data)
	# print (addData_df)
	# mysql에 session으로 데이터 추가
	dictToDf = pd.DataFrame(post_data, index=[0])
	# print(dictToDf.loc[0])
	# print(dictToDf.loc[1])
	# print(dictToDf.loc[2])
	# print(dictToDf.loc[3])
	print(dictToDf)

	table_name = 'dataset'
	dictToDf.to_sql (
				table_name,
				engine,
				if_exists='append',
				index=False,
				chunksize=500,
				method='multi'
			)
	return jsonify("hr")

if __name__ == '__main__':
    app.run(debug=True)