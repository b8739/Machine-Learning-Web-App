from flask import Flask, jsonify, request, render_template,request,url_for
from flask_cors import CORS

from flask_uploads import UploadSet,configure_uploads,IMAGES,DATA,ALL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import Integer, Text, String, DateTime
from sqlalchemy import create_engine, MetaData
from flask_migrate import Migrate

from werkzeug.utils  import secure_filename
import os
import datetime
import time


# EDA Packages
import pandas as pd 
import numpy as np 

# ML Packages
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC


# ML Packages For Vectorization of Text For Feature Extraction
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

# configuration
DEBUG = True


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configuration for File Uploads
files = UploadSet('files',ALL)
app.config['UPLOADED_FILES_DEST'] = 'static/uploadsDB'
configure_uploads(app,files)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/uploadsDB/filestorage.db'

# Saving Data To Database Storage
class FileContents(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(300))
	modeldata = db.Column(db.String(300))
	data = db.Column(db.LargeBinary)

def __repr__(self):
	return f"FileContents('{self.id}', '{self.name}', '{self.modeldata}', {self.data})"

class FileInfo (db.Model):
    id = db.Column(db.Integer,primary_key=True)

class DataSummary (db.Model):
    id = db.Column(db.Integer,primary_key=True)

# engine
engine = create_engine('sqlite:///static/uploadsDB/newfilestorage.db', echo = True)
meta = MetaData()

@app.route('/', methods=['GET'])
def testing():
	jobs_df = pd.read_csv('./static/uploadsDB/iris.csv')
	table_name = 'nyc'
	jobs_df.to_sql (
		table_name,
		engine,
		if_exists='replace',
		index=False,
		chunksize=500,
		dtype={
			"sepal_length": Integer,
			"sepal_width": Integer,
			"petal_length": Integer,
			"petal_width":  Integer,
			"species": Text
		}
	)
	meta.create_all(engine)
	return jsonify('pong!')

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

# Route for our Processing and Details Page
@app.route('/dataupload',methods=['GET','POST'])
def dataupload():
	if request.method == 'POST' and 'csv_data' in request.files:
		file = request.files['csv_data']
		filename = secure_filename(file.filename)
		# os.path.join is used so that paths work in every operating system
        # file.save(os.path.join("wherever","you","want",filename))
		file.save(os.path.join('static/uploadsDB',filename))
		fullfile = os.path.join('static/uploadsDB',filename)

		# For Time
		date = str(datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"))

		# EDA function
		df = pd.read_csv(os.path.join('static/uploadsDB',filename))
		df_size = df.size
		df_shape = df.shape
		df_columns = list(df.columns)
		df_targetname = df[df.columns[-1]].name
		df_featurenames = df_columns[0:-1] # select all columns till last column
		df_Xfeatures = df.iloc[:,0:-1] 
		df_Ylabels = df[df.columns[-1]] # Select the last column as target
		# same as above df_Ylabels = df.iloc[:,-1]
		

		# Model Building
		X = df_Xfeatures
		Y = df_Ylabels
		seed = 7
		# prepare models
		models = []
		models.append(('LR', LogisticRegression()))
		models.append(('LDA', LinearDiscriminantAnalysis()))
		models.append(('KNN', KNeighborsClassifier()))
		models.append(('CART', DecisionTreeClassifier()))
		models.append(('NB', GaussianNB()))
		models.append(('SVM', SVC()))
		# evaluate each model in turn
		

		results = []
		names = []
		allmodels = []
		scoring = 'accuracy'
		for name, model in models:
			kfold = model_selection.KFold(n_splits=10)
			cv_results = model_selection.cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
			results.append(cv_results)
			names.append(name)
			msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
			allmodels.append(msg)
			model_results = results
			model_names = names 
			
		# Saving Results of Uploaded Files to Sqlite DB
		newfile = FileContents(name=file.filename,data=file.read(),modeldata=msg)
		db.session.add(newfile)
		db.session.commit()
  
		dfplot = jsonify(df.to_dict())
	return jsonify(df.to_dict())
	# return render_template('details.html',filename=filename,date=date,
	# 	df_size=df_size,
	# 	df_shape=df_shape,
	# 	df_columns =df_columns,
	# 	df_targetname =df_targetname,
	# 	model_results = allmodels,
	# 	model_names = names,
	# 	fullfile = fullfile,
	# 	dfplot = df
	# 	)
@app.route('/checkDB',methods=['GET'])
def checkDatabase	():
    database = FileContents.query.all()
    return render_template('index.html', database=database)
#### 아래 라우팅 수정해서 Put이랑 Delete 만들면 됨####

# @app.route('/field/<field_id>', methods=['PUT', 'DELETE'])
# def single_book(book_id):
#     response_object = {'status': 'success'}
#     if request.method == 'PUT':
#         post_data = request.get_json()
#         remove_book(book_id)
#         BOOKS.append({
#             'id': uuid.uuid4().hex,
#             'title': post_data.get('title'),
#             'author': post_data.get('author'),
#             'read': post_data.get('read')
#         })
#         response_object['message'] = 'Book updated!'
#     if request.method == 'DELETE':
#         remove_book(book_id)
#         response_object['message'] = 'Book removed!'
#     return jsonify(response_object)

if __name__ == '__main__':
    app.run()