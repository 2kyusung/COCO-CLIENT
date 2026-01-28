import sys
import re
import json
import include.log as log
import include.utils as utils
import include.etl_exception as etl_exception
from include.query_stmt import QueryStmt
import channel.mysql.mysql_loader as mysql_loader
from datetime import datetime

class MysqlManagerCommon:

	def __init__(self, config, debug=True):		
		self.debug = debug
		self.filter_manager = None
		self.display_query = False
		self.db_loader = None
		self.db_connect_status = False
		self.loadDB(config, debug)

	def loadDB(self, config, debug):
		try:
			self.db_loader = mysql_loader.MySQLDBLoader(config, debug)
			self.db_connect_status = True
		except Exception as e:
			log.printException()

	def isDbConnected(self):
		return self.db_connect_status

	def setFilterManager(self, filter_manager):
		self.filter_manager = filter_manager

	def setDisplayQuery(self, display_query):
		self.display_query = display_query

	def isDisplayQuery(self):
		return self.display_query

	def setDebug(self, debug):
		self.debug = debug
		self.db_loader.setDebug(debug)
	
	def executeQuery(self, query, params=None, commit=True):
		try:
			# log.printLog(query, params)
			cursor = self.db_loader.getCursor()
			if params:
				if type(params) == tuple or type(params) == dict:
					cursor.execute(query, params=params)
				elif type(params) == list:
					cursor.executemany(query, params=params)
			else:
				cursor.execute(query)
			if commit:
				self.db_loader.commit()

			return cursor
		except Exception as e:
			log.printException(query)
		return False

	# Select 전용 Query Execute로 리턴 결과에 Field Name을 Mapping하여 가지고 온다.
	def executeQueryEx(self, query, params=None, date_to_str=False):
		result = []
		try:
			cursor = self.executeQuery(query, params, False)
			if cursor:
				row = cursor.fetchone()
				while row:
					cvt_item = self.return_dict_pair(cursor, row, date_to_str)
					result.append(cvt_item)
					row = cursor.fetchone()
				self.db_loader.commit()
				return result
			else:
				log.printLog("exceutQueryEx Cursor Error", type='error')
		except Exception as e:
			log.printException(query)
		
		return False		

	def addslashes(self, val, sub=re.compile(r"[\\\"']").sub):
		def fixup(m):
			return "\\" + m.group(0)
		return sub(fixup, val)	

	# value검사 직접 query를 조합하는 곳에서도 사용하기 위해서 static으로 제공함.
	def check_value(self, type, val, offset = None):
		try:
			if type == 's':
				val = QueryStmt.addslashes(val)
			elif type == 'i':
				if isinstance(val, str):
					float(utils.toNumber(val, "FLOAT"))
					val = val.replace(",", "")
				else:
					val = str(val)
		except Exception as e:
			log.printException(e)
			log.printLog(val)
			raise Exception
		return val

	def sql_array(self, ttype, val):
		try:
			if ttype == 's':
				if type(val) is str:
					val = ",".split(val)
				if type(val) is not list:
					return val
				r_val_list = []
				for v in val:
					r_val_list.append("'" + self.check_value('s', v) + "'")
				return ",".join(r_val_list)
			elif ttype == 'i':
				if type(val) is str:
					val = ",".split(val)
				if type(val) is not list:
					return val
				r_val_list = []
				for v in val:
					r_val_list.append(self.check_value('i', v))
				return ",".join(r_val_list)
		except Exception as e:
			log.printException(e)
			raise Exception
		return val

	def objToStr(self, obj, date_to_str):
		if date_to_str:
			if isinstance(obj, datetime):
				return obj.strftime('%Y-%m-%d %H:%M:%S')
			return obj
		else:
			return obj

	def return_dict_pair(self, cursor, row_item, date_to_str):
		if row_item:
			return_dict = {}
			for column_name, row in zip(cursor.description, row_item):
				return_dict[column_name[0]] = self.objToStr(row, date_to_str)
			return return_dict
		return None

	#  [{"key":"bon_rtime", "direction":"asc"}]
	#  * Order By문을 생성한다.
	def makeOrderBy(self, orderby_params, prefix=None):
		if not orderby_params:
			return ""
		orderby_params = utils.keyStrToUpper(orderby_params)  # KEY, DIRECTION을 대문자로 변환하기 위함.

		orderby = ""
		orderby_arr = []
		if(prefix):
			prefix += "."
		else:
			prefix = ""

		for value in orderby_params:
			orderby_arr.append(prefix + value['KEY'] + " " + value['DIRECTION'])

		if len(orderby_arr) == 0:
			return orderby
		orderby = "ORDER BY " + ",".join(orderby_arr)
		return orderby

	#  * Group By 문을 생성한다.
	def makeGroupBy(self, groupby_params, prefix=None):
		if not groupby_params:
			return ""

		groupby = ""
		groupby_arr = []
		if prefix:
			prefix += "."
		else:
			prefix = ""

		for value in groupby_params:
			groupby_arr.append(prefix + value)

		if len(groupby_arr) == 0:
			return groupby
		groupby = "GROUP BY " + ",".join(groupby_arr)
		return groupby

	#  * Range Where문을 생성한다.
	def getRange(self, key, gte=None, gt=None, lte=None, lt=None, type='NUMBER', prefix=None):
		range_arr = []
		try:
			if key and (gte!=None or gt!=None or lte!=None or lt!=None):
				if prefix:
					prefix += "."
				else:
					prefix = ""

				if gte != None:
					range_arr.append(prefix + key + ">=" + str(self.convertValue(gte, type)))
				if gt != None:
					range_arr.append(prefix + key + ">" + str(self.convertValue(gt, type)))
				if lte != None:
					range_arr.append(prefix + key + "<=" + str(self.convertValue(lte, type)))
				if lt != None:
					range_arr.append(prefix + key + "<" + str(self.convertValue(lt, type)))
		except Exception as e:
			log.printException()

		return range_arr

	#  * Value Type에 따라 Query 문에  문자열 TYPE은 '로 감싼다.
	def convertValue(self, value, type):
		query = ""
		try:
			type = type.upper()
			if type in ['TEXT', 'DATE', 'DATETIME']:
				if isinstance(value, datetime):
					query = "'" + value.strftime('%Y-%m-%d %H:%M:%S') + "'"
				else:
					cvt_value = self.check_value('s', value.strip())
					query = "'" + cvt_value + "'"
			elif type in ['NUMBER', 'INT', 'FLOAT']:
				cvt_value = self.check_value('i', str(value).strip())
				query = cvt_value
		except Exception as e:
			log.printException()
		return query

	def validateItem(self, value, type):
		# Type이 DATETIME, DATE, TIME인경우 VALUE가 날자 포맷을 가지는지 CHECK한다.
		if type.lower() in ['datetime', 'date', 'time'] and isinstance(value, str):
			try:
				cvt_value = utils.getDateFormat(date_format="", date_str=value)
				if cvt_value == None:
					log.printLog("This value is not Date Format", value)
					sys.exit()
				return cvt_value
			except Exception as e:
				pass
		return value

	# Insert into Query를 위해 Values를 구성하기 위한 함수.
	def convertValueForInsert(self, value, type):
		query = ""
		try:
			# String 값으로 NULL로 입력되어 있는 경우 또는 Value가 NULL인 경우 NULL 값으로 판단
			if value == None or (isinstance(value, str) and value.strip().upper() == 'NULL'):
				return 'NULL'

			type = type.upper()
			if type in ['TEXT', 'DATE', 'DATETIME']:
				if isinstance(value, datetime):
					query = "'" + value.strftime('%Y-%m-%d %H:%M:%S') + "'"
				elif type in ['DATE', 'DATETIME'] and isinstance(value, str):
					# Type이 DATETIME, DATE, TIME인경우 VALUE가 날자 포맷을 가지는지 CHECK한다.
					cvt_value = utils.getDateFormat(date_format='%Y-%m-%d %H:%M:%S', date_str=value)
					if cvt_value == None:
						# 추가되지 말아야 한다.
						raise etl_exception.RDBMSInsertException("Date Format Error : " + value)
					else:
						query = "'" + cvt_value + "'"
				else:
					if not isinstance(value, str):
						cvt_value = self.check_value('s', str(value).strip())
					else:
						cvt_value = self.check_value('s', value.strip())
					query = "'" + cvt_value + "'"
			elif type in ['NUMBER', 'INT', 'FLOAT']:
				cvt_value = self.check_value('i', str(value).strip())
				query = cvt_value
		except Exception as e:
			log.printException()
			raise etl_exception.RDBMSInsertDataConvertException("Date Format Error : " + value)
		return query

	def getEqual(self, key, data, prefix=None, is_not=False):
		try:
			type = "TEXT"
			value = None
			if isinstance(data, dict):
				type = data['TYPE']
				value = data['VALUE']
			else:
				value = data

			if prefix:
				prefix += "."
			else:
				prefix = ""

			if isinstance(value, list):
				value_not = ""
				if is_not:
					value_not = "NOT"
				# query = prefix + key + " " + value_not + " IN (" + S.SQL_IN_ARRAY(value, ",", type) + ")"
				cvt_value_list = []
				for v in value:
					cvt_value_list.append(self.convertValue(v, type))
				query = prefix + key + " " + value_not + " IN (" + ",".join(cvt_value_list) + ")"
			else:
				value_not = ""
				if is_not:
					value_not = "!"

				query = prefix + key + " " + value_not + "=" + self.convertValue(value, type)
			return query
		except Exception as e:
			log.printException()
		return ""

	def makeRangeQuery(self, range_params, prefix=None):
		where_arr = []
		try:
			for column_name, range_item in range_params.items():
				range_item = utils.keyStrToUpper(range_item)  # GT, GTE, LT, LTE를 모두 대문자로 변환한다.
				where_arr = where_arr + self.getRange(column_name, range_item.get('GTE', None), range_item.get('GT', None), range_item.get('LTE', None), range_item.get('LT', None), range_item.get('TYPE', 'TEXT'), prefix)
		except Exception as e:
			log.printException()
		return where_arr

	def makeWhereQuery(self, where_params, prefix=None):
		try:
			where_arr = []
			if where_params and isinstance(where_params, dict):
				for key, value in where_params.items():
					if key.upper() == "MUST":
						for must_key, must_value in value.items():
							if must_key == 'TERM':
								for tk, tv in must_value.items():
									where_arr.append(self.getEqual(tk, tv, prefix))
							elif must_key == 'RANGE':
								where_arr = where_arr + self.makeRangeQuery(must_value, prefix)
					elif key.upper() == "SHOULD":
						if value.get('TERM', None) != None:
							for tk, tv in value['TERM'].items():
								where_arr.append(self.getEqual(tk, tv, prefix))
					elif key.upper() == "MUST_NOT":
						if value.get('TERM', None) != None:
							for tk, tv in value['TERM'].items():
								where_arr.append(self.getEqual(tk, tv, prefix, True))
					elif key.upper() == "RANGE_LIST":
						should_range_where_list = []
						for should_range_item in value:
							should_range_where_list.append(self.makeWhereQuery(should_range_item, prefix))
						where_arr.append("(" + ") OR (".join(should_range_where_list) + ")")
					else:
						where_arr.append(self.getEqual(key, value, prefix))

			if len(where_arr) == 0:
				return '1'

			where = " AND ".join(where_arr)

			return where
		except Exception as e:
			log.printException()
			return '1'

	def getCommonList(self, table_name, where_params, orderby_params, groupby_params, limit_size, field_list='*', curpage=0):
		try:
			where = self.makeWhereQuery(where_params)
			orderby = self.makeOrderBy(orderby_params)
			groupby = self.makeGroupBy(groupby_params)

			if limit_size > 0:
				if curpage == 0:  # bookmark field가 존재한다.
					query = F"SELECT {field_list} FROM {table_name} WHERE {where} {groupby} {orderby} LIMIT {limit_size}"
				else:
					offset = (curpage-1)*limit_size
					query = F"SELECT {field_list} FROM {table_name} WHERE {where} {groupby} {orderby} LIMIT {offset}, {limit_size}"
			else:
				query = F"SELECT {field_list} FROM {table_name} WHERE {where} {groupby} {orderby}"

			# log.printLog(query)
			if self.display_query:
				log.printLog(query)
				return True

			response = self.executeQueryEx(query)
			if response == False:
				return False
			return response
		except Exception as e:
			log.printException()
		return False

	#  * Table을 비운다.
	#  * @param  [type] table_name [description]
	#  * @return [type]             [description]
	def truncateTable(self, table_name):
		if not table_name:
			return False
		query = F"TRUNCATE TABLE {table_name}"
		response = self.executeQuery(query)
		if response == False:
			return False
		return True

	def deleteCommon(self, table_name, where_params):
		where = self.makeWhereQuery(where_params)
		query = F"DELETE FROM {table_name} WHERE {where}"

		if self.display_query:
			log.printLog(query)
			return True

		response = self.executeQuery(query)
		if response == False:
			return False
		return True

	# Insert시 Filter 적용을 위해
	def applyFilterItem(self, value, filter, value_list=None):
		if self.filter_manager:
			return self.filter_manager.applyFilter(value, filter, value_list)
		return value

	def makeInsertValueList(self, field_list, data_list):
		try:
			cvt_data_list = []
			for v in data_list:
				cvt_item = []
				try:
					for fitem in field_list:				
						if v.get(fitem['SOURCE']['NAME'], None) != None:
							# SyncLogger::addLog(fitem['SOURCE']['NAME'])
							cvt_item.append(self.convertValueForInsert(self.applyFilterItem(v[fitem['SOURCE']['NAME']], fitem['FILTER'], v), fitem['TARGET']['TYPE']))
						else:
							cvt_item.append(self.convertValueForInsert(self.applyFilterItem(fitem['DEFAULT'], fitem['FILTER'], v), fitem['TARGET']['TYPE']))
					cvt_data_list.append(",".join(cvt_item))
				except etl_exception.RDBMSInsertDataConvertException as e:
					# RDBMSInsertException이 발생했다면 해당 Data를 Insert Error Log에 저장한다.
					log.Log.insertLog("INSERT", " ".join(e.args) , json.dumps(v))
					log.printException(e)
				except Exception as e:
					log.printException(e)
					log.printLog(v)
			# log.printLog(cvt_data_list)
			# for v in cvt_data_list:
			# 	log.printLog(v)
			return "(" + "),(".join(cvt_data_list) + ")"
		except Exception as e:
			log.printException(e)
		return False

	def makeInsertFieldList(self, field_list):
		field_name_list = []
		for v in field_list:
			field_name_list.append(v['TARGET']['NAME'])

		return "(`" + '`,`'.join(field_name_list) + '`)'

	def insertBulk(self, table_name, field_list, data_list):
		try:
			log.printLog("InsertBulk : " + str(len(data_list)))
			insert_field_list = self.makeInsertFieldList(field_list)
			insert_data_list = self.makeInsertValueList(field_list, data_list)
			query = F"INSERT INTO {table_name} {insert_field_list} VALUES {insert_data_list}"

			if self.display_query:
				log.printLog(query)
				return True
			response = self.executeQuery(query, None, True)
			if response == False:
				return False
			return True
		except Exception as e:
			log.printException()
		return False
		

	def makeDeleteKeyList(self, delete_key, data_list):
		delete_key_name = delete_key['SOURCE_NAME']
		delete_key_type = delete_key['TYPE']

		delete_value_list = {}
		for v in data_list:
			delete_value_list[v[delete_key_name]] = self.convertValue(v[delete_key_name], delete_key_type)

		if len(delete_value_list) == 0:
			return False

		return ",".join(delete_value_list)

	def deleteRange(self, table_name, where_params):
		where = self.makeWhereQuery(where_params)

		query = F"DELETE FROM {table_name} WHERE {where}"

		if self.display_query:
			log.printLog(query)
			return True
		response = self.executeQuery(query)
		if response == False:
			return False
		return True

	def deleteBulk(self, table_name, where_params, delete_key, data_list):
		where = self.makeWhereQuery(where_params)

		delete_data_where_list = self.makeDeleteKeyList(delete_key, data_list)
		if delete_data_where_list == False:
			return False

		delete_key_name = delete_key['TARGET_NAME']

		query = F"DELETE FROM {table_name} WHERE {where} AND {delete_key_name} in ({delete_data_where_list})"

		if self.display_query:
			log.printLog(query)
			return True
		response = self.executeQuery(query)
		if response == False:
			return False
		return True	
	
	# 2개 이상의 값을 비교해야 해야 하는 경우 
	def deleteCommonKeyValue(self, table_name, delete_list):
		try:
			where = ""
			where_arr = []
			for item in delete_list:
				item_list = []
				for k, v in item.items():
					item_list.append(k + "='" + self.check_value('s', v) + "'")
				where_arr.append("(" + " AND ".join(item_list) + ")")
			where = " OR ".join(where_arr)
			
			if where:
				query = F"""DELETE FROM {table_name} WHERE {where}"""
				
				response = self.executeQueryEx(query)
				if response == False:
					return False
				return response
		except Exception as e:
			log.printException(e)

		return False

	def getDateCount(self, table_name, start_date, end_date, key_field):
		try:
			if table_name and start_date and end_date and key_field:
				query = F"SELECT date_format({key_field}, '%Y-%m-%d') as {key_field}, count(*) as cnt FROM {table_name} where {key_field}>='{start_date}' and {key_field}<='{end_date}' group by date_format({key_field}, '%Y-%m-%d')"
				response = self.executeQueryEx(query)
				if response == False:
					return False
				return response
		except Exception as e:
			log.printException(e)
		
		return False

	def insertCocoErrorLog(self, msg, wholesale_site=None, product_code=None, mall_pid=None, target_mall=None):
		try:

			if not wholesale_site:
				wholesale_site = ""
			if not product_code:
				product_code = ""
			if not mall_pid:
				mall_pid = ""
			if not target_mall:
				target_mall = ""
			if msg == None:
				msg = ""

			query = F"INSERT INTO error_log (wholesale_site, product_code, mall_pid, target_mall, error_message, rtime) VALUES ('{wholesale_site}', '{product_code}', '{mall_pid}', '{target_mall}', '{msg}', NOW())"

			if self.display_query:
				log.printLog(query)
				return True

			response = self.executeQuery(query, None, True)
			if response == False:
				return False
			return True
		except Exception as e:
			log.printException(e)
		return False