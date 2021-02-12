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

# EDA function
dataset_df = pd.read_csv(os.path.join('static/uploadsDB',filename))
table_name = 'Dataset'

# dataset_df_size = dataset_df.size
# dataset_df_shape = dataset_df.shape
# dataset_df_columns = list(dataset_df.columns)
# dataset_df_targetname = dataset_df[dataset_df.columns[-1]].name
# dataset_df_featurenames = dataset_df_columns[0:-1] # select all columns till last column
# dataset_df_Xfeatures = dataset_df.iloc[:,0:-1] 
# dataset_df_Ylabels = dataset_df[dataset_df.columns[-1]] # Select the last column as target
# # same as above df_Ylabels = df.iloc[:,-1]

# # Model Building
# X = dataset_df_Xfeatures
# Y = dataset_df_Ylabels
# seed = 7
# # prepare models
# models = []
# models.append(('LR', LogisticRegression()))
# models.append(('LDA', LinearDiscriminantAnalysis()))
# models.append(('KNN', KNeighborsClassifier()))
# models.append(('CART', DecisionTreeClassifier()))
# models.append(('NB', GaussianNB()))
# models.append(('SVM', SVC()))
# # evaluate each model in turn

# results = []
# names = []
# allmodels = []
# scoring = 'accuracy'
# for name, model in models:
#     kfold = model_selection.KFold(n_splits=10)
#     cv_results = model_selection.cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
#     results.append(cv_results)
#     names.append(name)
#     msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
#     allmodels.append(msg)
#     model_results = results
#     model_names = names 
# # 	df_size=df_size,
# # 	df_shape=df_shape,
# # 	df_columns =df_columns,
# # 	df_targetname =df_targetname,
# # 	model_results = allmodels,
# # 	model_names = names,
# # 	fullfile = fullfile,
# # 	dfplot = df