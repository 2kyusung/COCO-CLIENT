import base64
import include.utils as utils
import datetime
from urllib import parse as url_parser
import include.log as log
from include.content_loader import ContentLoader
from config import ConfigCommon

class ApiManager:
	def __init__(self):
		try:
			pass
		except Exception as e:
			log.printException(e)

	def getImageSavePath(self, params):
		try:
			user_id = params.get("user_id", None)
			url = ConfigCommon.HOST_ADDR + "/index.php?c=API&sc=GET_IMAGE_SAVE_PATH&proc=1"

			headers = {
				"accept": "*/*",
				"accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
				"cache-control": "no-cache",
				"logic": "PART",
				"pragma": "no-cache",
				"referer": ConfigCommon.HOST_ADDR,
				"sec-fetch-dest": "empty",
				"sec-fetch-mode": "cors",
				"sec-ch-ua-mobile": "?0",
				'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
				"logic": "PART",
				"sec-fetch-site": "same-origin",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
			}
			# user_agent = ""
			referer = ConfigCommon.HOST_ADDR
			# cookies = None
			# timeout = (5, 15)
			# allow_redirects = True
			method = "POST"
			postdata = {"user_id":user_id}
			# data_type = None
			# proxy setting
			use_proxy = True
			# proxy = {'http':"socks5://socks.marketingtool.co.kr:10000", 'https':"socks5://socks.marketingtool.co.kr:10000"}
			proxy = None
			response = ContentLoader.getContent(url, headers=headers, referer=referer, method=method, proxy=proxy, postdata=postdata)
			
			return response.text

		except Exception as e:
			log.printException(e)

		return None

	def getDomeProductList(self, params):
		try:
			user_id = params.get("user_id", None)
			url = ConfigCommon.HOST_ADDR + "/index.php?c=API&sc=GET_DOME_PRODUCT_LIST&proc=1"

			headers = {
				"accept": "*/*",
				"accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
				"cache-control": "no-cache",
				"logic": "PART",
				"pragma": "no-cache",
				"referer": ConfigCommon.HOST_ADDR,
				"sec-fetch-dest": "empty",
				"sec-fetch-mode": "cors",
				"sec-ch-ua-mobile": "?0",
				'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
				"logic": "PART",
				"sec-fetch-site": "same-origin",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
			}
			# user_agent = ""
			referer = ConfigCommon.HOST_ADDR
			# cookies = None
			# timeout = (5, 15)
			# allow_redirects = True
			method = "POST"
			postdata = {"user_id":user_id}
			# data_type = None
			# proxy setting
			use_proxy = True
			# proxy = {'http':"socks5://socks.marketingtool.co.kr:10000", 'https':"socks5://socks.marketingtool.co.kr:10000"}
			proxy = None
			response = ContentLoader.getContent(url, headers=headers, referer=referer, method=method, proxy=proxy, postdata=postdata)
			
			return response.text

		except Exception as e:
			log.printException(e)

		return None

	def getCheckTagList(self, params):
		try:
			user_id = params.get("user_id", None)
			url = ConfigCommon.HOST_ADDR + "/index.php?c=API&sc=GET_CHECK_TAG_LIST&proc=1"

			headers = {
				"accept": "*/*",
				"accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
				"cache-control": "no-cache",
				"logic": "PART",
				"pragma": "no-cache",
				"referer": ConfigCommon.HOST_ADDR,
				"sec-fetch-dest": "empty",
				"sec-fetch-mode": "cors",
				"sec-ch-ua-mobile": "?0",
				'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
				"logic": "PART",
				"sec-fetch-site": "same-origin",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
			}
			# user_agent = ""
			referer = ConfigCommon.HOST_ADDR
			# cookies = None
			# timeout = (5, 15)
			# allow_redirects = True
			method = "POST"
			postdata = {"user_id":user_id}
			# data_type = None
			# proxy setting
			use_proxy = True
			# proxy = {'http':"socks5://socks.marketingtool.co.kr:10000", 'https':"socks5://socks.marketingtool.co.kr:10000"}
			proxy = None
			response = ContentLoader.getContent(url, headers=headers, referer=referer, method=method, proxy=proxy, postdata=postdata)
			
			return response.text

		except Exception as e:
			log.printException(e)

		return None

	def updateCheckTagList(self, params):
		try:
			user_id = params.get("user_id", None)
			keyword_list = params.get("keyword_list", [])
			url = ConfigCommon.HOST_ADDR + "/index.php?c=API&sc=UPDATE_CHECKED_TAG_LIST&proc=1"

			headers = {
				"accept": "*/*",
				"accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
				"cache-control": "no-cache",
				"logic": "PART",
				"pragma": "no-cache",
				"referer": ConfigCommon.HOST_ADDR,
				"sec-fetch-dest": "empty",
				"sec-fetch-mode": "cors",
				"sec-ch-ua-mobile": "?0",
				'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
				"logic": "PART",
				"sec-fetch-site": "same-origin",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
			}
			# user_agent = ""
			referer = ConfigCommon.HOST_ADDR
			# cookies = None
			# timeout = (5, 15)
			# allow_redirects = True
			method = "POST"
			postdata = {"user_id":user_id, "keyword_list":keyword_list}
			# data_type = None
			# proxy setting
			use_proxy = True
			# proxy = {'http':"socks5://socks.marketingtool.co.kr:10000", 'https':"socks5://socks.marketingtool.co.kr:10000"}
			proxy = None
			response = ContentLoader.getContent(url, headers=headers, referer=referer, method=method, proxy=proxy, postdata=postdata)
			
			return response.text

		except Exception as e:
			log.printException(e)

		return None
	
	def getCheckTitleList(self, params):
		try:
			user_id = params.get("user_id", None)
			url = ConfigCommon.HOST_ADDR + "/index.php?c=API&sc=GET_CHECK_TITLE_LIST&proc=1"

			headers = {
				"accept": "*/*",
				"accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
				"cache-control": "no-cache",
				"logic": "PART",
				"pragma": "no-cache",
				"referer": ConfigCommon.HOST_ADDR,
				"sec-fetch-dest": "empty",
				"sec-fetch-mode": "cors",
				"sec-ch-ua-mobile": "?0",
				'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
				"logic": "PART",
				"sec-fetch-site": "same-origin",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
			}
			# user_agent = ""
			referer = ConfigCommon.HOST_ADDR
			# cookies = None
			# timeout = (5, 15)
			# allow_redirects = True
			method = "POST"
			postdata = {"user_id":user_id}
			# data_type = None
			# proxy setting
			use_proxy = True
			# proxy = {'http':"socks5://socks.marketingtool.co.kr:10000", 'https':"socks5://socks.marketingtool.co.kr:10000"}
			proxy = None
			response = ContentLoader.getContent(url, headers=headers, referer=referer, method=method, proxy=proxy, postdata=postdata)
			
			return response.text

		except Exception as e:
			log.printException(e)

		return None

	def updateCheckTitleList(self, params):
		try:
			user_id = params.get("user_id", None)
			keyword_list = params.get("keyword_list", [])
			url = ConfigCommon.HOST_ADDR + "/index.php?c=API&sc=UPDATE_CHECKED_TITLE_LIST&proc=1"

			headers = {
				"accept": "*/*",
				"accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
				"cache-control": "no-cache",
				"logic": "PART",
				"pragma": "no-cache",
				"referer": ConfigCommon.HOST_ADDR,
				"sec-fetch-dest": "empty",
				"sec-fetch-mode": "cors",
				"sec-ch-ua-mobile": "?0",
				'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
				"logic": "PART",
				"sec-fetch-site": "same-origin",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
			}
			# user_agent = ""
			referer = ConfigCommon.HOST_ADDR
			# cookies = None
			# timeout = (5, 15)
			# allow_redirects = True
			method = "POST"
			postdata = {"user_id":user_id, "keyword_list":keyword_list}
			# data_type = None
			# proxy setting
			use_proxy = True
			# proxy = {'http':"socks5://socks.marketingtool.co.kr:10000", 'https':"socks5://socks.marketingtool.co.kr:10000"}
			proxy = None
			response = ContentLoader.getContent(url, headers=headers, referer=referer, method=method, proxy=proxy, postdata=postdata)
			
			return response.text

		except Exception as e:
			log.printException(e)

		return None
	
	# Coco With People Word Count를 조사할 목록을 가지고 온다.
	def getWordCountCheckList(self, params):
		try:
			user_id = params.get("user_id", None)
			url = ConfigCommon.HOST_ADDR + "/index.php?c=API&sc=GET_CHECK_WORD_COUNT_LIST&proc=1"

			headers = {
				"accept": "*/*",
				"accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
				"cache-control": "no-cache",
				"logic": "PART",
				"pragma": "no-cache",
				"referer": ConfigCommon.HOST_ADDR,
				"sec-fetch-dest": "empty",
				"sec-fetch-mode": "cors",
				"sec-ch-ua-mobile": "?0",
				'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
				"logic": "PART",
				"sec-fetch-site": "same-origin",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
			}
			# user_agent = ""
			referer = ConfigCommon.HOST_ADDR
			# cookies = None
			# timeout = (5, 15)
			# allow_redirects = True
			method = "POST"
			postdata = {"user_id":user_id}
			# data_type = None
			# proxy setting
			use_proxy = True
			# proxy = {'http':"socks5://socks.marketingtool.co.kr:10000", 'https':"socks5://socks.marketingtool.co.kr:10000"}
			proxy = None
			response = ContentLoader.getContent(url, headers=headers, referer=referer, method=method, proxy=proxy, postdata=postdata)
			
			return response.text

		except Exception as e:
			log.printException(e)

		return None

	def updateWordCountCheckList(self, params):
		try:
			user_id = params.get("user_id", None)
			keyword_list = params.get("keyword_list", [])
			url = ConfigCommon.HOST_ADDR + "/index.php?c=API&sc=UPDATE_CHECKED_WORD_COUNT&proc=1"

			headers = {
				"accept": "*/*",
				"accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
				"cache-control": "no-cache",
				"logic": "PART",
				"pragma": "no-cache",
				"referer": ConfigCommon.HOST_ADDR,
				"sec-fetch-dest": "empty",
				"sec-fetch-mode": "cors",
				"sec-ch-ua-mobile": "?0",
				'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
				"logic": "PART",
				"sec-fetch-site": "same-origin",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
			}
			# user_agent = ""
			referer = ConfigCommon.HOST_ADDR
			# cookies = None
			# timeout = (5, 15)
			# allow_redirects = True
			method = "POST"
			postdata = {"user_id":user_id, "keyword_list":keyword_list}
			# data_type = None
			# proxy setting
			use_proxy = True
			# proxy = {'http':"socks5://socks.marketingtool.co.kr:10000", 'https':"socks5://socks.marketingtool.co.kr:10000"}
			proxy = None
			response = ContentLoader.getContent(url, headers=headers, referer=referer, method=method, proxy=proxy, postdata=postdata)
			
			return response.text

		except Exception as e:
			log.printException(e)

		return None


	###########################################################################################################################################################
	
	# Naver Smartstore에서 동일 키워드 3개를 조합하여 하나의 키워드가 몇개의 단어로 구성되어 있는지를 조사한다.
	def parsingCheckWordCount(self, params):
		try:
			keyword = params.get("keyword", None)
			encoded_keyword = url_parser.quote(keyword)
			cookies = params.get("cookies", None)
			url = F"https://sell.smartstore.naver.com/api/product/shared/product-search-quality-check?_action=productSearchQualityCheck&category1Id=50000008&category2Id=50000056&category3Id=50000949&category4Id=50004132&prodNm=" + encoded_keyword
			headers = {
				"accept": "*/*",
				"accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
				"cache-control": "no-cache",
				"logic": "PART",
				"pragma": "no-cache",
				"referer": F"https://sell.smartstore.naver.com/",
				"sec-fetch-dest": "empty",
				"sec-fetch-mode": "cors",
				"sec-ch-ua-mobile": "?0",
				'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
				"logic": "PART",
				"sec-fetch-site": "same-origin",
				"X-Current-State": "https://sell.smartstore.naver.com/#/products/create",
				"X-Current-Statename": "main.product.create",
				"X-To-Statename": "main.product.create",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
			}
			# user_agent = ""
			referer = F"https://sell.smartstore.naver.com/"
			# cookies = None
			# timeout = (5, 15)
			# allow_redirects = True
			method = "GET"
			# postdata = None
			# data_type = None
			# proxy setting
			use_proxy = True
			# proxy = {'http':"socks5://socks.marketingtool.co.kr:10000", 'https':"socks5://socks.marketingtool.co.kr:10000"}
			proxy = None
			response = ContentLoader.getContent(url, headers=headers, referer=referer, method=method, proxy=proxy, cookies=cookies)
			
			return response.text

		except Exception as e:
			log.printException(e)

		return None
	
	def parsingCheckTag(self, params):
		try:
			keyword_list = params.get("keyword_list", None)
			tag_query = ""
			for keyword in keyword_list:
				encoded_keyword = url_parser.quote(keyword)
				tag_query += "&tags=" + encoded_keyword
			cookies = params.get("cookies", None)
			url = F"https://sell.smartstore.naver.com/api/product/shared/check-searchable-tags?_action=checkSearchableTags" + tag_query

			log.printLog(url)
			headers = {
				"accept": "*/*",
				"accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
				"cache-control": "no-cache",
				"logic": "PART",
				"pragma": "no-cache",
				"referer": F"https://sell.smartstore.naver.com/",
				"sec-fetch-dest": "empty",
				"sec-fetch-mode": "cors",
				"sec-ch-ua-mobile": "?0",
				'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
				"logic": "PART",
				"sec-fetch-site": "same-origin",
				"X-Current-State": "https://sell.smartstore.naver.com/#/products/create",
				"X-Current-Statename": "main.product.create",
				"X-To-Statename": "main.product.create",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
			}
			# user_agent = ""
			referer = F"https://sell.smartstore.naver.com/"
			# cookies = None
			# timeout = (5, 15)
			# allow_redirects = True
			method = "GET"
			# postdata = None
			# data_type = None
			# proxy setting
			use_proxy = True
			# proxy = {'http':"socks5://socks.marketingtool.co.kr:10000", 'https':"socks5://socks.marketingtool.co.kr:10000"}
			proxy = None
			response = ContentLoader.getContent(url, headers=headers, referer=referer, method=method, proxy=proxy, cookies=cookies)
			log.printLog(response)
			return response.text

		except Exception as e:
			log.printException(e)

		return None
	
	#################################################################################################################################################
	# 수집 아이템을 가지고 온다.
	def getCrawlingItemList(self, params):
		try:
			client_id = params.get("client_id", None)
			size = params.get("size", 1)
			debug = params.get("debug", 1)
			timestamp = str(datetime.datetime.now())

			url = ConfigCommon.HOST_ADDR + F"/index.php?c=API&sc=KEYWORD_LIST&proc=1&size={size}&client_id={client_id}&debug={debug}&_t={timestamp}"

			headers = {
				"accept": "*/*",
				"accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
				"cache-control": "no-cache",
				"logic": "PART",
				"pragma": "no-cache",
				"referer": ConfigCommon.HOST_ADDR,
				"sec-fetch-dest": "empty",
				"sec-fetch-mode": "cors",
				"sec-ch-ua-mobile": "?0",
				'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
				"logic": "PART",
				"sec-fetch-site": "same-origin",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
			}
			# user_agent = ""
			referer = ConfigCommon.HOST_ADDR
			# cookies = None
			# timeout = (5, 15)
			# allow_redirects = True
			method = "GET"
			# data_type = None
			# proxy setting
			use_proxy = True
			# proxy = {'http':"socks5://socks.marketingtool.co.kr:10000", 'https':"socks5://socks.marketingtool.co.kr:10000"}
			proxy = None
			response = ContentLoader.getContent(url, headers=headers, referer=referer, method=method, proxy=proxy)
			
			return response.text

		except Exception as e:
			log.printException(e)

		return None
	
	# 수집 아이템을 가지고 온다.
	def sendKeywordPageList(self, params):
		try:
			client_id = params.get("client_id", None)
			page = params.get("page", 1)
			next_data = params.get("next_data", None)
			keyword = params.get("keyword", None)
			seq = params.get("seq", None)
			user_id = params.get("user_id", None)
			status = params.get("status", None)
			target = params.get("target", None)

			# next_data = utils.zipArchive(next_data)
			next_data_base64 = base64.b64encode(next_data.encode('utf-8')).decode('utf-8')

			timestamp = str(datetime.datetime.now())

			url = ConfigCommon.HOST_ADDR + F"/index.php?c=API&sc=INSERT_NAVER_KEYWORD_LIST&proc=1&_t={timestamp}"
			if target == "keyword_tag":
				url = ConfigCommon.HOST_ADDR + F"/index.php?c=API&sc=INSERT_NAVER_KEYWORD_TAG_LIST&proc=1&_t={timestamp}"
			log.printLog(url)
			headers = {
				"accept": "*/*",
				"accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
				"cache-control": "no-cache",
				"logic": "PART",
				"pragma": "no-cache",
				"referer": ConfigCommon.HOST_ADDR,
				"sec-fetch-dest": "empty",
				"sec-fetch-mode": "cors",
				"sec-ch-ua-mobile": "?0",
				'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
				"logic": "PART",
				"sec-fetch-site": "same-origin",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
			}
			# user_agent = ""
			referer = ConfigCommon.HOST_ADDR
			# cookies = None
			# timeout = (5, 15)
			# allow_redirects = True
			method = "POST"
			postdata = {
				"client_id":client_id, 
				"page":page,
				"next_data":next_data_base64,
				"keyword":keyword,
				"seq":seq,
				"user_id":user_id,
				"status":status,
				"target":target,
				"debug":0
				}
			# data_type = None
			# proxy setting
			use_proxy = True
			# proxy = {'http':"socks5://socks.marketingtool.co.kr:10000", 'https':"socks5://socks.marketingtool.co.kr:10000"}
			proxy = None
			response = ContentLoader.getContent(url, headers=headers, referer=referer, method=method, proxy=proxy, postdata=postdata)
			
			return response.text

		except Exception as e:
			log.printException(e)

		return None

	# 수집 TAG DATA를 전달한다.
	def sendTagList(self, params):
		try:
			client_id = params.get("client_id", None)
			keyword = params.get("keyword", None)
			tag_data = params.get("tag_data", None)
			seq = params.get("seq", None)
			user_id = params.get("user_id", None)
			status = params.get("status", None)
			target = params.get("target", None)

			timestamp = str(datetime.datetime.now())

			url = ConfigCommon.HOST_ADDR + F"/index.php?c=API&sc=INSERT_TAG_LIST&proc=1&_t={timestamp}"

			headers = {
				"accept": "*/*",
				"accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
				"cache-control": "no-cache",
				"logic": "PART",
				"pragma": "no-cache",
				"referer": ConfigCommon.HOST_ADDR,
				"sec-fetch-dest": "empty",
				"sec-fetch-mode": "cors",
				"sec-ch-ua-mobile": "?0",
				'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
				"logic": "PART",
				"sec-fetch-site": "same-origin",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
			}
			# user_agent = ""
			referer = ConfigCommon.HOST_ADDR
			# cookies = None
			# timeout = (5, 15)
			# allow_redirects = True
			method = "POST"
			postdata = {
				"client_id":client_id, 
				"keyword":keyword,
				"tag_data":tag_data,
				"seq":seq,
				"user_id":user_id,
				"status":status,
				"target":target
				}
			# data_type = None
			# proxy setting
			use_proxy = True
			# proxy = {'http':"socks5://socks.marketingtool.co.kr:10000", 'https':"socks5://socks.marketingtool.co.kr:10000"}
			proxy = None
			response = ContentLoader.getContent(url, headers=headers, referer=referer, method=method, proxy=proxy, postdata=postdata)
			
			return response.text

		except Exception as e:
			log.printException(e)

		return None
	
	# 수집 아이템을 가지고 온다.
	def updateCrawlingStatus(self, params):
		try:
			client_id = params.get("client_id", None)
			user_id = params.get("user_id", None)
			keyword = params.get("keyword", None)
			page = params.get("page", None)
			seq = params.get("seq", None)
			target = params.get("target", None)	
			status = params.get("status", None)

			timestamp = str(datetime.datetime.now())

			url = ConfigCommon.HOST_ADDR + F"/index.php?c=API&sc=UPDATE_CRAWLING_STATUS&proc=1&_t={timestamp}"

			headers = {
				"accept": "*/*",
				"accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
				"cache-control": "no-cache",
				"logic": "PART",
				"pragma": "no-cache",
				"referer": ConfigCommon.HOST_ADDR,
				"sec-fetch-dest": "empty",
				"sec-fetch-mode": "cors",
				"sec-ch-ua-mobile": "?0",
				'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
				"logic": "PART",
				"sec-fetch-site": "same-origin",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
			}
			# user_agent = ""
			referer = ConfigCommon.HOST_ADDR
			# cookies = None
			# timeout = (5, 15)
			# allow_redirects = True
			method = "POST"
			postdata = {
				"client_id":client_id, 
				"user_id":user_id,
				"keyword":keyword,
				"page":page,
				"seq":seq,
				"status":status,
				"target":target
				}
			# data_type = None
			# proxy setting
			use_proxy = True
			# proxy = {'http':"socks5://socks.marketingtool.co.kr:10000", 'https':"socks5://socks.marketingtool.co.kr:10000"}
			proxy = None
			response = ContentLoader.getContent(url, headers=headers, referer=referer, method=method, proxy=proxy, postdata=postdata)
			
			return response.text

		except Exception as e:
			log.printException(e)

		return None