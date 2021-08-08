"""
RDS
"""
# config.py
datasetsInfo = {
    'user'     : 'dbUser',		# 1)
    'password' : 'atticdatabase',		# 2)
    'host'     : 'aa10d3zbjwjmj1b.ckbsxxh58sws.ap-northeast-2.rds.amazonaws.com',	# 3)
    'port'     : 3306,			# 4)
    'database' : 'datasets'		# 5)
}

datasets_URL = f"mysql+mysqlconnector://{datasetsInfo['user']}:{datasetsInfo['password']}@{datasetsInfo['host']}:{datasetsInfo['port']}/{datasetsInfo['database']}?charset=utf8"

# config.py
modelingInfo = {
    'user'     : 'dbUser',		# 1)
    'password' : 'atticdatabase',		# 2)
    'host'     : 'aa10d3zbjwjmj1b.ckbsxxh58sws.ap-northeast-2.rds.amazonaws.com',	# 3)
    'port'     : 3306,			# 4)
    'database' : 'project_1'		# 5)
}

modeling_URL = f"mysql+mysqlconnector://{modelingInfo['user']}:{modelingInfo['password']}@{modelingInfo['host']}:{modelingInfo['port']}/{modelingInfo['database']}?charset=utf8"

"""
Local
"""

# URI_dataset = 'mysql+mysqldb://root:0000@localhost/datasets'
# URI_modeling = 'mysql+mysqldb://root:0000@localhost/project_1'