import linecache
import sys
import re
import inspect
import pprint
from pathlib import Path
import datetime
from config import ConfigCommon
import os.path, time
from channel.mysql.mysql_manager import MysqlManagerCommon

def printException(*args, exit_program=False):
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)

	msg = ""
	for arg in args:
		if msg :
			msg += " "
		if isinstance(arg, Exception):
			msg += "Exception Type : " + type(arg).__name__ + " - "
		msg += str(arg)

	exception_str = '{} [ERROR] EXCEPTION IN ({}, LINE {} "{}"): {}'.format(str(datetime.datetime.now()), filename, lineno, line.strip(), exc_obj)
	print(exception_str)
	Log.printLog(exception_str)
	if len(msg) > 0 :
		print(str(datetime.datetime.now()), filename, "LINE", lineno, "[INFO]", msg)
		Log.printLog(str(datetime.datetime.now()), filename, "LINE", lineno, "[INFO]", msg)

	if exit_program == True:
		exit()
	return exception_str

def printLog(*args, **kargs):
	try:
		callerframerecord = inspect.stack()[1]    # 0 represents this line
												# 1 represents line at caller
		frame = callerframerecord[0]
		info = inspect.getframeinfo(frame)
		file_info = Path(info.filename)
		
		lineno = info.lineno
		filename = file_info.name

		msg = ""
		for arg in args:
			if msg :
				msg += " "
			msg += str(arg)
		
		msg_type = kargs.get('type', 'info')
		if msg_type.lower() == "info":
			msg_type = "INFO"
		elif msg_type.lower() == "error" or msg_type.lower() == "err":
			msg_type = "ERROR"
		else:
			msg_type = "INFO"

		if len(args) == 1 and (isinstance(args[0], dict) or isinstance(args[0], list) or isinstance(args[0], tuple)):
			print(str(datetime.datetime.now()), filename, "LINE", lineno, "[" + msg_type + "]")
			pprint.pprint(args[0], width=20, indent=4)
		else:
			print(str(datetime.datetime.now()), filename, "LINE", lineno, "[" + msg_type + "]", msg)

		Log.printLog(str(datetime.datetime.now()), filename, "LINE", lineno, "[" + msg_type + "]", msg)
	except Exception as e:
		print("Exception PrintLog")


def printClass(item):
	printLog(type(item))
	printLog(dir(item))

class Log:
	target = ""
	dbm = None
	group_id = ""
	prefix = ""

	def __init__(self):
		pass

	@classmethod
	def setGroupId(cls, group_id):
		cls.group_id = group_id

	@classmethod
	def setPrefix(cls, prefix):
		cls.prefix = prefix

	@classmethod
	def insertLog(cls, log_type, msg, value):
		try:
			if isinstance(value, str):
				if cls.dbm == None:
					cls.dbm = MysqlManagerCommon(ConfigCommon.LOG_INFO.get('DB_INFO', None))				
				
				table_name = ConfigCommon.LOG_INFO.get('DB_TABLE_NAME', None)
				field_list = ConfigCommon.LOG_INFO.get('DB_FIELD_LIST', None)
				data_list = [{"prefix":Log.prefix, "group_id":Log.group_id, "log_type":log_type, "msg":msg, "item_value":value, "rtime":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]
				cls.dbm.insertBulk(table_name, field_list, data_list)
		except Exception as e:
			pass

	@classmethod
	def getLogFileName(self):
		pass

	@classmethod
	def printLog(self, *args):
		try:
			if ConfigCommon.LOG_INFO.get('ENABLE', False) == True:
				msg = ""
				for arg in args:
					if msg :
						msg += " "
					msg += str(arg)
				today = datetime.datetime.now().strftime('%Y%m%d')
				# log_file_name = "Log_" + today + ".log"
				# log_path = ConfigCommon.LOG_INFO.get('PATH', None)
				# with open(log_path + "/" + log_file_name, "a", -1, 'utf-8') as f:
				# 	f.write(msg)
				# 	f.write("\n")
		except Exception as e:
			pprint.pprint("Error : Log Class printLog")

	# 보관 기간이 지난 로그파일을 지운다.
	@classmethod
	def deleteLogFile(self):
		if ConfigCommon.LOG_INFO.get('ENABLE', False) == True:
			today = datetime.datetime.today()
			storage_period = ConfigCommon.LOG_INFO.get('STORAGE_PERIOD', 10)
			log_delete_day = today - datetime.timedelta(days = storage_period)
			log_path = ConfigCommon.LOG_INFO.get('PATH', None)
			file_list = os.listdir(log_path)

			for file in file_list:			
				if log_delete_day > datetime.datetime.fromtimestamp(os.path.getmtime(log_path + "/" + file)):
					os.remove(log_path + "/" + file)

		# print ("file_list: {}".format(file_list))
		# 생성일 기준으로 삭제.
		# print "last modified: %s" % time.ctime(os.path.getmtime(file))
		# print "created: %s" % time.ctime(os.path.getctime(file))

		