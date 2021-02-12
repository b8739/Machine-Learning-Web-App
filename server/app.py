from flask import Flask, jsonify, request, render_template,request,url_for
from flask_cors import CORS

from flask_uploads import UploadSet,configure_uploads,IMAGES,DATA,ALL
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine, MetaData, text
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

# engine
engine = create_engine('mysql+mysqldb://root:root@localhost/newdatabase',echo = True)

@app.route('/', methods=['GET'])
def testing():
	return jsonify('Hello World!')

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

# Route for our Processing and Details Page
@app.route('/dataupload',methods=['GET','POST'])
def dataupload():
	if request.method == 'POST' and 'csv_data' in request.files:
		file = request.files['csv_data']

		# pandas
		dataset_df = pd.read_csv(file)
		table_name = 'Dataset'

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
 
@app.route('/checkDB',methods=['GET'])
def checkDatabase	():
    database = Dataset.query.all()
    return render_template('index.html', database=database)

if __name__ == '__main__':
    app.run()