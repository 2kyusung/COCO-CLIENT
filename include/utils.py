import io
import zipfile
import linecache
import sys
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta
import calendar
import inspect
from pathlib import Path
import pprint
import chardet
import json
from urllib import parse

import include.log as log
from include.content_loader import ContentLoader

pp = pprint.PrettyPrinter(indent=4)

def removeEmoji(input_data):
	# return input_data.encode('utf-8', 'ignore').decode('utf-8')
	emoji_list = ['🥃','🤣','🤗','🤭','🥲','🫡','🦌','🤪','🥵','🤔','🫣','🤩','😀','😃','🥺','😀','😁','😂','🤣','😃','😄','😅','😆','😉','😊','😋','😎','😍','😘','🥰','😗','😙','😚','☺','🙂','🤗','🤩','🤔','🤨','😐','😑','😶','🙄','😏','😣','😥','😮','🤐','😯','😪','😫','🥱','😴','😌','😛','😜','😝','🤤','😒','😓','😔','😕','🙃','🤑','😲','☹','🙁','😖','😞','😟','😤','😢','😭','😦','😧','😨','😩','🤯','😬','😰','😱','🥵','🥶','😳','🤪','😵','🥴','😠','😡','🤬','😷','🤒','🤕','🤢','🤮','🤧','😇','🥳','🥺','🤠','🤡','🤥','🤫','🤭','🧐','🤓','😈','👿','👹','👺','💀','☠','👻','👽','👾','🤖','💩','😺','😸','😹','😻','😼','😽','🙀','😿','😾','🐱‍👤','🐱‍🏍','🐱‍💻','🐱‍🐉','🐱‍👓','🐱‍🚀','🙈','🙉','🙊','🐵','🐶','🐺','🐱','🦁','🐯','🦒','🦊','🦝','🐮','🐷','🐗','🐭','🐹','🐰','🐻','🐨','🐼','🐸','🦓','🐴','🦄','🐔','🐲','🐽','🐾','🐒','🦍','🦧','🦮','🐕‍🦺','🐩','🐕','🐈','🐅','🐆','🐎','🦌','🦏','🦛','🐂','🐃','🐄','🐖','🐏','🐑','🐐','🐪','🐫','🦙','🦘','🦥','🦨','🦡','🐘','🐁','🐀','🦔','🐇','🐿','🦎','🐊','🐢','🐍','🐉','🦕','🦖','🦦','🦈','🐬','🐳','🐋','🐟','🐠','🐡','🦐','🦑','🐙','🦞','🦀','🐚','🦆','🐓','🦃','🦅','🕊','🦢','🦜','🦩','🦚','🦉','🐦','🐧','🐥','🐤','🐣','🦇','🦋','🐌','🐛','🦟','🦗','🐜','🐝','🐞','🦂','🕷','🕸','🦠','🧞‍♀️','🧞‍♂️','🗣','👤','👥','👁','👀','🦴','🦷','👅','👄','🧠','🦾','🦿','👣','🤺','⛷','🤼‍♂️','🤼‍♀️','🫠','🥹','🤦‍♀️','🫢','🤜','🤛']
	

	for emoji in emoji_list:
		input_data = input_data.replace(emoji, "")
	return input_data.encode('utf-8', 'ignore').decode('utf-8')

def zipArchive(text):
	# 텍스트를 바이트로 변환
	text_bytes = text.encode('utf-8')

	# 메모리 내에서 압축된 데이터를 저장하기 위한 BytesIO 객체 생성
	compressed_data = io.BytesIO()

	# BytesIO 객체를 zipfile로 압축
	with zipfile.ZipFile(compressed_data, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
		# zip파일 안에 파일명을 지정하고 텍스트를 기록
		zf.writestr('text.txt', text_bytes)

	# 압축된 데이터를 변수에 저장
	compressed_text = compressed_data.getvalue()

	return compressed_text

def download(url, file_name):
	try:
		with open(file_name, "wb") as file:   # open in binary mode
			headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
				"accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
				"cache-control": "no-cache",
				"Connection": "keep-alive",
				"logic": "PART",
				"pragma": "no-cache",
				'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
				"sec-ch-ua-mobile": "?0",
				"sec-fetch-dest": "empty",
				"sec-fetch-mode": "cors",
				"sec-fetch-site": "same-site",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}
			# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
			# cookies = None
			# timeout = (5, 15)
			# allow_redirects = True
			method = "GET"
			# data_type = None
			# proxy setting
			# us_proxy = False
			# proxy = None
			response = ContentLoader.getContent(url, headers=headers, method=method)
			file.write(response.content)      # write to file
	except Exception as e:
		log.printException(e)

def printException(*args):
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
		msg += str(arg)

	exception_str = '{} [ERROR] EXCEPTION IN ({}, LINE {} "{}"): {}'.format(str(datetime.now()), filename, lineno, line.strip(), exc_obj)
	print(exception_str)
	log.printLog(exception_str)
	if len(msg) > 0 :
		print(str(datetime.now()), filename, "LINE", lineno, "[INFO]", msg)
		log.printLog(str(datetime.now()), filename, "LINE", lineno, "[INFO]", msg)

def printLog(*args, **kargs):
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


	print(str(datetime.now()), filename, "LINE", lineno, "[" + msg_type + "]", msg)
	log.printLog(str(datetime.now()), filename, "LINE", lineno, "[" + msg_type + "]", msg)

# Price가 포함된 String에서 Price에 해당하는 부분만 추출한다.
# 통화 단위를 입력받아 표준 체계로 변환함.
def standardCurrency(cur_type, s):
	if s == None :
		return 0

	cur_type = cur_type.upper()
	s = s.strip()	

	# -- 숫자에 관여하는 데이터가 아닌 것은 제거함.
	convert_str = ""
	# b = bytearray()
	# b.extend(map(ord, s))
	# for num in b:
	# 	print(num)
	# 	if (num >= 0x30 and num <= 0x39) or chr(num) == "," or chr(num) == "." :
	# 		convert_str += chr(num)
	for num in s:
		if (num >= '0' and num <= '9') or num == "," or num == "." :
			convert_str += num

	if cur_type == "EUR" or cur_type == "COP" or cur_type == "RP" or cur_type == "VND" or cur_type == "IDR" :
		# -- 유로화는 .는 천단위, 콤마(,)는 소숫점임.
		# -- 인도네시아 IDR(RP), 베트남 VND 추가
		convert_str = convert_str.replace(".", "")
		convert_str = convert_str.replace(",", ".")
	else :
		# -- 콤마는 제거함
		convert_str = convert_str.replace(",", "")
	
	result_value = float(convert_str)
	if result_value == None :
		return 0
	return result_value
    
# 문자를 숫자로 변경한다.
# 입력한 문자열 중 수자가 아닌 문자는 삭제하고 숫자로 치환한다.
# num type : int, float
def toNumber(str_val, num_type="INT"):
	if str_val == None :
		return 0
	if isinstance(str_val, str) == False:
		return str_val

	num_type = num_type.upper()
	str_val = str_val.strip()	

	# -- 숫자에 관여하는 데이터가 아닌 것은 제거함.
	convert_str = ""
	# b = bytearray()
	# b.extend(map(ord, s))
	# for num in b:
	# 	print(num)
	# 	if (num >= 0x30 and num <= 0x39) or chr(num) == "," or chr(num) == "." :
	# 		convert_str += chr(num)
	for num in str_val:
		if (num >= '0' and num <= '9') or num == "," or num == "." or num == "-":
			convert_str += num

	# -- 콤마는 제거함
	convert_str = convert_str.replace(",", "")

	if not num_type:
		num_type = "INT"

	if num_type == "INT":
		result_value = int(convert_str)
	elif num_type == "FLOAT":
		result_value = float(convert_str)
	else:
		result_value = int(convert_str)
		
	if result_value == None :
		return 0
	return result_value

# 문자열 앞에 0으로 시작하면 0을 삭제한다.
def ltrimZero(txt):
	result_value = None
	try:
		x = re.search(r"[0]*(.+)", txt)
		if x != None:
			t = x.groups()
			result_value = t[0]
	except Exception as e:
		pass
	return result_value


def regularText(txt):	
	txt = txt.strip()
	txt = re.sub(r'\s', " ", txt)
	txt = re.sub(r'\s\s', " ", txt)
	return txt.strip()

def ListGenerator(data, index = None):
	if data == None :
		return None
		
	if type(data) == str :
		data = [data]
	
	if index != None and type(index) == int :
		if len(data) > index:
			try:
				return data[index]
			except Exception as e:
				return None
		else:
			return None

	return data

# File의 Encoding을 확인한다.
# 전체 데이터를 읽어 판단하기 때문에 파일 사이즈가 큰경우 분석 시간이 오래 걸림
def findFileEncoding(file_path):
	try:
		rawdata = open(file_path, 'rb').read()
		result = chardet.detect(rawdata)
		charenc = result['encoding']
		return charenc
	except Exception as e:
		printException()
	return None

# 다중 Dictionary에 설정되어 있는 값을 List Type의 Key List로 가져오기 위한 함수
# ex)
# 	getDictValue(config_data, ['MULTI_PROCESSING', 'WORKER_SIZE'], 1)
def getDictValue(dict_obj, keys, default=None):
	try:
		item = dict_obj
		index = 0
		key_len = len(keys)
		if key_len == 0:
			return default

		for key in keys:
			index += 1
			if index >= key_len:
				item = item.get(key, default)
			else:
				item = item.get(key, {})

		return item
	except Exception as e:
		return default

def calcTime(target_date, convert_type, value):
	try:
		if type(target_date) == str:
			target_date = datetime.strptime(target_date, "%Y-%m-%d")
		elif type(target_date) == datetime:
			target_date = target_date
		else:
			print("ERROR Unknown Date")
			return None

		if convert_type == "month":
			year = target_date.year
			month = target_date.month
			if month + value <= 0:
				year -= 1
				month = 12 + month + value
			elif month + value > 12:
				year += 1
				month = month + value - 12
			else:
				month = month + value

			target_date = target_date.replace(year=year, month=month)
	except Exception as e:
		print(e, year, month)
	
	return target_date


# Date String을 Format String으로 변환한다.
def getDateFormat(date_format=None, date_str=None, add_months=None, add_days=None, add_hours=None, input_date_format=None):
	try:
		if input_date_format:
			st_datetime = datetime.strptime(date_str, input_date_format)
		else:
			try:
				st_datetime = datetime.strptime(date_str, "%Y-%m-%d")
			except Exception as e:
				try:
					st_datetime = datetime.strptime(date_str, "%Y%m%d")
				except Exception as e:
					try:
						st_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
					except Exception as e:
						st_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")

		if add_months != None:
			st_datetime = st_datetime + relativedelta(months=add_months)
		if add_days != None:
			st_datetime = st_datetime + relativedelta(days=add_days)
		if add_hours != None:
			st_datetime = st_datetime + relativedelta(hours=add_hours)

		if date_format == None:
			return st_datetime
		return st_datetime.strftime(date_format)
	except Exception as e:
		log.printException(e, date_str)
	return None

# 입력한 날짜 문자열을 년도와 월, 월의 마지막 날짜로 변경하여 리턴한다.
def getDateFormatForMonth(date_str, hour_format="00:00:00"):
	try:
		st_datetime = datetime.strptime(date_str, "%Y-%m-%d")
	except Exception as e:
		try:
			st_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
		except Exception as e:
			st_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")

	last_day_of_month = calendar.monthrange(st_datetime.year, st_datetime.month)[1]

	if hour_format == None:
		return st_datetime.strftime('%Y-%m-' + str(last_day_of_month).zfill(2))	
	return st_datetime.strftime('%Y-%m-' + str(last_day_of_month).zfill(2) + " " + hour_format)


# /**
#  * Array의 Key를 모두 대문자로 변경하여 리턴한다.
#  * @param  [type] $params_tmp [description]
#  * @return [type]             [description]
#  */
def keyStrToUpper(params_tmp):
	if not isinstance(params_tmp, list) and not isinstance(params_tmp, dict):
		return params_tmp

	if isinstance(params_tmp, list):
		params = []
		for v in params_tmp:
			if isinstance(v, list) or isinstance(v, dict):
				v = keyStrToUpper(v)
			params.append(v)

		return params
		
	if isinstance(params_tmp, dict):
		params = {}
		for k, v in params_tmp.items():
			if isinstance(v, list) or isinstance(v, dict):
				v = keyStrToUpper(v)
			params[k.upper()] = v
		return params

	return params_tmp

#  * 파일명을 Format에 맞게 변경하여 리턴한다.
#  * 현재 날짜를 추가, 추출 기간의 Target date를 추가, 추출 필드 값을 포함등
#  * @param  [type] $file_name   [description]
#  * @param  array  $item        [description]
#  * @param  array  $ext_params  [description]
#  * @param  [type] $target_date [description]
#  * @return [type]              [description]
def convertFileName(file_name, item={}, ext_params={}, target_date=None):
	if item and isinstance(item, dict):
		for k, v in item.items(): 
			if isinstance(v, str):
				file_name = file_name.replace("#" + k + "#", v)
	if ext_params and isinstance(ext_params, dict):
		for k, v in ext_params.items():
			if isinstance(v, str):
				file_name = file_name.replace("#" + k + "#", v)

	if target_date == None:
		# Target Date가 설정되어 있지 않다면 오늘 날짜로 설정한다.
		target_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	date_format = getDateFormat("%y%m%d", target_date)
	file_name = file_name.replace("#YYMMDD#", date_format)

	date_format = getDateFormat("%Y%m%d", target_date)
	file_name = file_name.replace("#YYYYMMDD#", date_format)

	date_format = getDateFormat("%Y%m%d_%H%M%S", target_date)
	file_name = file_name.replace("#YYYYMMDD_HHIISS#", date_format)

	# 오늘 날짜를 가지고 온다.
	today_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	date_format = getDateFormat("%Y%m%d", today_datetime)
	file_name = file_name.replace("#TODAY_YYYYMMDD#", date_format)

	date_format = getDateFormat("%Y%m%d_%H%M%S", today_datetime)
	file_name = file_name.replace("#TODAY_YYYYMMDD_HHIISS#", date_format)

	return file_name

#  * [convertType description]
#  * @param  [type] $type [description]
#  * @return [type]       [description]
def convertType(type):
	new_type = "TEXT"
	if type in ["varchar", "nvarchar", "char", "json", "tinytext", "date", "time", "datetime"]:
		new_type = "TEXT"
	elif type in ["bigint", "mediumint", "smallint", "tinyint", "int", "double", "float", "number", "numeric"]:
		new_type = "NUMBER"
	else:
		log.printLog("NEW TYPE : " + type)
	return new_type

def makeFieldListByArray(params):
	field_list = []
	for k, v in params.items():
		if isinstance(v, dict):
			sk = ''
			sv = ''
			tk = ''
			tv = ''

			for tsk, tsv in v['source'].items():
				sk = tsk
				sv = tsv
				break

			for tsk, tsv in v['target'].items():
				tk = tsk
				tv = tsv
				break

			field_list.append(json.dumps(
				{
				"SOURCE":{"NAME":sk, "TYPE":convertType(sv)},
				"TARGET":{"NAME":tk, "TYPE":convertType(tv)},
				"DEFAULT":"",
				"FILTER":[],
				"DESCRIPT":""
				}
			))
		else:
			field_list.append(json.dumps(
				{
				"SOURCE":{"NAME":k, "TYPE":convertType(v)},
				"TARGET":{"NAME":k, "TYPE":convertType(v)},
				"DEFAULT":"",
				"FILTER":[],
				"DESCRIPT":""
				}
			))

	for v in field_list:
		log.printLog(v + ",")

def makeFieldList(params):
	if isinstance(params, dict):
		makeFieldListByArray(params)
		return

	field_list = []
	scheme_list = params.split(",")
	for v in scheme_list:
		v = re.sub("COMMENT.*", "", v, flags=re.IGNORECASE)
		matched = re.search(r"[\[`]*(\w+)[\]`]*\s+(\w+).*DEFAULT\s+'(.*)'", v, flags=re.IGNORECASE)
		if matched != None:
			field_list.append(
				{
				"SOURCE":{"NAME":matched.groups()[0], "TYPE":matched.groups()[1]},
				"TARGET":{"NAME":matched.groups()[0], "TYPE":matched.groups()[1]},
				"DEFAULT":matched.groups()[2],
				"FILTER":[],
				"DESCRIPT":""
				}
			)
		else:
			matched = re.search(r"[\[`]*(\w+)[\]`]*\s+(\w+)", v, flags=re.IGNORECASE)
			if matched != None:
				field_list.append(
					{
					"SOURCE":{"NAME":matched.groups()[0], "TYPE":matched.groups()[1]},
					"TARGET":{"NAME":matched.groups()[0], "TYPE":matched.groups()[1]},
					"DEFAULT":"",
					"FILTER":[],
					"DESCRIPT":""
					}
				)

	for v in field_list:
		log.printLog(v + ",")


def getBiggestItem(item_list):
    item = None
    index = -1
    for vi in range(0, len(item_list)):
        vitem = item_list[vi]
        if item == None:
            item = vitem
            index = vi
        elif item.get('count') < vitem.get('count'):
            item = vitem
            index = vi
    
    item_list.remove(item)
    item_list.insert(0, item)
    return item_list

def parserUrl(url):
	url_info = {'path':'', 'params':{}}
	try:
		url_infos = parse.urlparse(url)
		param_info = parse.parse_qs(url_infos.query)

		for v in param_info.items():
			key = v[0]
			val = v[1][0]
			url_info['params'][key] = val
	except Exception as e:
		log.printException(e)
	return url_info