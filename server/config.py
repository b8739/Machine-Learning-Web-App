"""
RDS
"""

# datasetsInfo = {
#     'user'     : 'dbUser',		# 1)
#     'password' : 'atticdatabase',		# 2)
#     'host'     : 'aabs8zfdf421wt.ckbsxxh58sws.ap-northeast-2.rds.amazonaws.com',	# 3)
#     'port'     : 3306,			# 4)
#     'database' : 'datasets'		# 5)
# }

# datasets_URL = f"mysql+mysqlconnector://{datasetsInfo['user']}:{datasetsInfo['password']}@{datasetsInfo['host']}:{datasetsInfo['port']}/{datasetsInfo['database']}?charset=utf8"


# modelingInfo = {
#     'user'     : 'dbUser',		# 1)
#     'password' : 'atticdatabase',		# 2)
#     'host'     : 'aabs8zfdf421wt.ckbsxxh58sws.ap-northeast-2.rds.amazonaws.com',	# 3)
#     'port'     : 3306,			# 4)
#     'database' : 'project_1'		# 5)
# }

# modeling_URL = f"mysql+mysqlconnector://{modelingInfo['user']}:{modelingInfo['password']}@{modelingInfo['host']}:{modelingInfo['port']}/{modelingInfo['database']}?charset=utf8"

# auditingInfo = {
#     'user'     : 'dbUser',		# 1)
#     'password' : 'atticdatabase',		# 2)
#     'host'     : 'aabs8zfdf421wt.ckbsxxh58sws.ap-northeast-2.rds.amazonaws.com',	# 3)
#     'port'     : 3306,			# 4)
#     'database' : 'auditing'		# 5)
# }

# auditing_URL = f"mysql+mysqlconnector://{auditingInfo['user']}:{auditingInfo['password']}@{auditingInfo['host']}:{auditingInfo['port']}/{auditingInfo['database']}?charset=utf8"

# """
# Local
# """

datasets_URL = 'mysql+mysqldb://root:0000@localhost/datasets'
modeling_URL = 'mysql+mysqldb://root:0000@localhost/project_1'
