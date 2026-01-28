
# Library List
#
# Date Util
# 	pip install python-dateutil
#
# Elasticsearch Client
#	pip install elasticsearch
# 
# Mysql Connector : Mysql Connector 
# 	pip install mysql-connector
#
# Mssql Connector : Mssql Python
#   pip install pymssql
#
# Requests : Curl
#   pip install requests
# Requests Socks Proxy 설정을 위한 Lib
#	pip install 'requests[socks]'
#
# File Encoding을 Detect하기 위한 Lib
# pypi.org/project/chardet/
#	pip install chardet
#
# A python implementation of SSHv2. for SFTP
# http://www.paramiko.org/index.html
# pip install paramiko
#
# Web Driver Path 정보.
# File에서 읽어오는 방식으로 변경 필요.

# Excel Read library
# pip install xlrd
# pip install xlwt
# pip install openpyxl
# pip install pandas

# XPath 사용을 위한 lxml
# pip install lxml

# slack client
# pip install slackclient

# image library
# pip install pillow

# Web Crawler 관련
# pip install selenium==4.14.0
# pip install selenium webdriver_manager

# pip install PyQt5

# 클립 보드 사용
# pip install pyperclip

# Exe File 생성
# pip install -U pyinstaller

# EXE File 생성 방법
# pyinstaller -w -F run.py

class ConfigCommon:
	LOG_INFO = {
		"ENABLE":False,
		"TYPE": "MYSQL", 
		"DB_INFO": {
			"id": "shield",
			"password": "shield000",
			"host": "192.168.0.214:3306",
			"db_name": "ETL"
		},
		"DB_TABLE_NAME": "etl_log",
		"DB_FIELD_LIST": [
			{"SOURCE": {"NAME": "prefix", "TYPE": "TEXT"}, "TARGET": {"NAME": "prefix", "TYPE": "TEXT"}, "DEFAULT": "", "FILTER": [], "DESCRIPT": ""},
			{"SOURCE": {"NAME": "group_id", "TYPE": "TEXT"}, "TARGET": {"NAME": "group_id", "TYPE": "TEXT"}, "DEFAULT": "", "FILTER": [], "DESCRIPT": ""},
			{"SOURCE": {"NAME": "log_type", "TYPE": "TEXT"}, "TARGET": {"NAME": "log_type", "TYPE": "TEXT"}, "DEFAULT": "", "FILTER": [], "DESCRIPT": ""},
			{"SOURCE": {"NAME": "msg", "TYPE": "TEXT"}, "TARGET": {"NAME": "msg", "TYPE": "TEXT"}, "DEFAULT": "", "FILTER": [], "DESCRIPT": ""},
			{"SOURCE": {"NAME": "item_value", "TYPE": "TEXT"}, "TARGET": {"NAME": "item_value", "TYPE": "TEXT"}, "DEFAULT": "", "FILTER": [], "DESCRIPT": ""},
			{"SOURCE": {"NAME": "rtime", "TYPE": "DATETIME"}, "TARGET": {"NAME": "rtime", "TYPE": "DATETIME"}, "DEFAULT": "", "FILTER": [], "DESCRIPT": ""},
		],
		"PATH":"C:\\Project\\Log",		# Log File 저장 위치.
		"STORAGE_PERIOD":7,				# Log File 보관 기간 단위 : Day (보관 기간 이후 삭제함)
	}

	PROXY_INFO = {
		"socks" : {
			"address": "socks.marketingtool.co.kr",
			"port":10000
		}
	}
	
	USER_INFO = {
		"COCOWITHPEOPLE": {
			"user_id" : ""	# dev2.cocowithpeople.co.kr 접속 ID
		},
		"SMARTSTORE": {
			"user_id" : "",		# smart store 접속 ID
			"password" : ""		# smart store 접속 PASSWORD
		}
	}

	CRAWLER_MODE = False

	HOST_ADDR = "http://www.cocowithpeople.co.kr"

	@classmethod
	def getSmartstoreUserInfo(cls, info):
		return cls.USER_INFO.get('SMARTSTORE', {}).get(info, '')
	
	@classmethod
	def setSmartstoreUserInfo(cls, info, value):
		cls.USER_INFO['SMARTSTORE'][info] = value
	
	@classmethod
	def getCocoWithPeopleUserInfo(cls, info):
		return cls.USER_INFO.get('COCOWITHPEOPLE', {}).get(info, '')
	
	@classmethod
	def setCocoWithPeopleUserInfo(cls, info, value):
		cls.USER_INFO['COCOWITHPEOPLE'][info] = value

	@classmethod
	def setCrawlerMode(cls, mode):
		cls.CRAWLER_MODE = mode

	@classmethod
	def getCrawlerMode(cls):
		return cls.CRAWLER_MODE

		
