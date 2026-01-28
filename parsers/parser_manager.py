import pprint
import threading
import time
import re
import json
import pyperclip
from collections import deque
from datetime import datetime
import include.log as log
from include.load_driver import DriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchWindowException
from include.content_loader import ContentLoader
from api.api_manager import ApiManager
from config import ConfigCommon
# from crawler.script.common.parser_config import *


from pathlib import Path
from typing import Dict
import requests





class ParserManager:
	def __init__(self, browser_name, headless=True, worker=None, debug=True): 
		self.MAIN_SLEEP_TIME = 0.1
		self.browser_name = browser_name
		self.headless = headless
		self.driverManager = DriverManager(browser_name, headless)
		self.apiManager = ApiManager()
		self.stop_loop = False
		self.debug = True
		self.loop_count = 0
		self.sender = None
		self.worker = worker

	def setDebug(self, debug):
		self.debug = debug

	# def getParser(self, site):
	# 	parser = None

	# 	try:
	# 		module_name = site.replace(".", "_")
	# 		print(module_name)
	# 		parser = __import__('crawler.script.%s' %(module_name), fromlist=[module_name])
	# 		return parser.Parser(self.driverManager, self.redirectionManager)
	# 	except Exception as e:
	# 		log.printException()

	# 	return None
	
	def quit(self):
		print("Exit Program")
		self.driverManager.stop()

	def resetDriver(self):
		self.driverManager = DriverManager(self.browser_name, self.headless)

	def refresh(self):
		try:
			browser = self.driverManager.driver
			browser.refresh()
		except Exception as e:
			log.printException(e)
	def checkLogin(self):
		for _ in range(1,3):
			need_login = False
			try:
				browser = self.driverManager.driver
				try:
					if browser.current_window_handle == None:
						log.printLog("Browser is None")
				except Exception as e:
					self.resetDriver()
					browser = self.driverManager.driver
					
				find_login_id = browser.find_element(By.XPATH, "//a[@ui-sref='main.seller-member']/span[contains(@class,'login-id')]")
			except Exception as e:
				log.printException(e)
				need_login = True
			if need_login:
				self.loginSmartstore()
			else:
				return True
		return False

	def loginSmartstore(self):
		try:
			browser = self.driverManager.driver
			browser.get("https://sell.smartstore.naver.com/")
			time.sleep(2)
			btn_login = browser.find_element(By.XPATH, "//button[contains(@class, 'btn-login')]")
			btn_login.click()
			time.sleep(2)
			pyperclip.copy(ConfigCommon.getSmartstoreUserInfo('user_id'))	# "cocowithpeople@gmail.com"
			input_id = browser.find_element(By.XPATH, "//input[@class='Login_ipt__6a-x7' and @type='text']")
			input_id.send_keys(Keys.CONTROL, "v")
			time.sleep(2)
			pyperclip.copy(ConfigCommon.getSmartstoreUserInfo('password'))	# "Dlrkdnjs102&"
			input_id = browser.find_element(By.XPATH, "//input[@class='Login_ipt__6a-x7' and @type='password']")
			input_id.send_keys(Keys.CONTROL, "v")
			time.sleep(2)
			btn_login = browser.find_element(By.XPATH, "//div[@class='Login_btn_box__fgb5v']/button")
			btn_login.click()
			time.sleep(3)
			# 2단계 인증 필요 여부
			# TextField_btn_certify__2GCpl
			try:
				while(True):
					btn_certify = browser.find_element(By.XPATH, "//button[@class='TextField_btn_certify__2GCpl']")
					time.sleep(2)
			except Exception as e:
				time.sleep(2)
		except Exception as e:
			log.printException(e)

	def getCookies(self):
		try:
			res_data = {}
			browser = self.driverManager.driver
			cookie_list = browser.get_cookies()
			for cookie in cookie_list:
				cookie_name = cookie.get('name', None)
				cookie_value = cookie.get('value', None)
				res_data[cookie_name] = cookie_value
			return res_data
		except Exception as e:
			log.printException(e)
		return None
	
	# 키워드를 구성하는 단어 개수를 조사한다.
	def checkWordCount(self, keyword_list):
		try:
			checked_login = self.checkLogin()
			if checked_login == False:
				# 5번 로그인 시도를 했지만 로그인을 하지 못했다.
				# 파서 확인 또는 2차 인증 확인이 필요 (2차 인증도 검증 로직을 추가하자)
				log.printLog("로그인 실패 : 파서 또는 2차 인증 확인 필요")
			else:
				log.printLog("로그인 성공")
				browser = self.driverManager.driver
				browser.get("https://sell.smartstore.naver.com/#/products/create")
				time.sleep(2)

				keyword_count = len(keyword_list)
				ind = 1
				checked_keyword_list = []
				for keyword in keyword_list:
					try:
						for _ in range(1,5):
							res_data = self.apiManager.parsingCheckWordCount({'cookies':self.getCookies(), 'keyword':keyword + ' ' + keyword + ' ' + keyword})
							if res_data:
								break
							time.sleep(0.5)
						log.printLog(res_data)
						res_data_json = json.loads(res_data)
						total_score = res_data_json.get("result", {}).get("totalScore", None)
						cause_list = res_data_json.get("result", {}).get("cause", [])

						checked_keyword = {'keyword':keyword, 'word_count':0, 'split_keyword':''}
						if len(cause_list) == 0:
							checked_keyword['word_count'] = 1
						else:
							for cause in cause_list:
								cause_msg = cause.get("cause", None)
								if cause_msg == "유의어 포함 반복된 단어가 다수 포함되어 있습니다.":
									term = cause.get("term", None)
									if len(term) > 0:
										checked_keyword['word_count'] = len(term)
										checked_keyword['split_keyword'] = ",".join(term)
									break
						checked_keyword_list.append(checked_keyword)
						self.worker.sendLog(str(ind)+"/"+str(keyword_count)+" : "+keyword)
						ind += 1
						time.sleep(0.5)
					except Exception as e:
						log.printException(e)

				return checked_keyword_list			

		except Exception as e:
			log.printException(e)
		return None
	
	# 조합 타이틀이 사용 가능하지 체크 한다.
	def checkCombineTitle(self, keyword_list):
		try:
			checked_login = self.checkLogin()
			if checked_login == False:
				# 5번 로그인 시도를 했지만 로그인을 하지 못했다.
				# 파서 확인 또는 2차 인증 확인이 필요 (2차 인증도 검증 로직을 추가하자)
				log.printLog("로그인 실패 : 파서 또는 2차 인증 확인 필요")
			else:
				log.printLog("로그인 성공")
				browser = self.driverManager.driver
				browser.get("https://sell.smartstore.naver.com/#/products/create")
				time.sleep(2)
				checked_keyword_list = []
				keyword_count = len(keyword_list)
				ind = 1
				for keyword in keyword_list:
					try:
						for _ in range(1,5):
							res_data = self.apiManager.parsingCheckWordCount({'cookies':self.getCookies(), 'keyword':keyword})
							if res_data:
								break
							time.sleep(0.5)
						# log.printLog(res_data)
						res_data_json = json.loads(res_data)
						total_score = res_data_json.get("result", {}).get("totalScore", None)
						cause_list = res_data_json.get("result", {}).get("cause", [])

						checked_keyword = {'keyword':keyword, 'usable':0, 'cause':''}
						if len(cause_list) == 0 :
							checked_keyword['usable'] = 1
						else:
							for cause in cause_list:
								checked_keyword['cause'] = cause.get("cause", "")
								checked_keyword['cause'] += " (" + ", ".join(cause.get("term", [])) + ")"
								break
						checked_keyword_list.append(checked_keyword)
						self.worker.sendLog(str(ind)+"/"+str(keyword_count)+" : "+keyword)
						ind += 1
						time.sleep(0.5)
					except Exception as e:
						log.printException(e)

				return checked_keyword_list			

		except Exception as e:
			log.printException(e)
		return None
	
	# TAG 사용 여부를 체크한다.
	def checkTag(self, keyword_list):
		try:
			checked_login = self.checkLogin()
			if checked_login == False:
				# 5번 로그인 시도를 했지만 로그인을 하지 못했다.
				# 파서 확인 또는 2차 인증 확인이 필요 (2차 인증도 검증 로직을 추가하자)
				log.printLog("로그인 실패 : 파서 또는 2차 인증 확인 필요")
			else:
				log.printLog("로그인 성공")
				browser = self.driverManager.driver
				browser.get("https://sell.smartstore.naver.com/#/products/create")
				time.sleep(2)
				checked_keyword_list = []
				
				try:
					for _ in range(1,5):
						res_data = self.apiManager.parsingCheckTag({'cookies':self.getCookies(), 'keyword_list':keyword_list})
						if res_data:
							break
						time.sleep(0.5)
					res_data_json = json.loads(res_data)
					res_tag_list = []
					for v in res_data_json:
						res_tag = v.get('tag', None)
						if res_tag:
							res_tag_list.append(res_tag)

					for keyword in keyword_list:
						if keyword in res_tag_list:
							checked_keyword_list.append({'keyword':keyword, 'usable':1})
						else:
							checked_keyword_list.append({'keyword':keyword, 'usable':0})
				except Exception as e:
					log.printException(e)

				return checked_keyword_list			

		except Exception as e:
			log.printException(e)
		return None

	
	def uploadImage(self, file_path: str) -> str:
		"""
		SmartStore 에디터 토큰/세션키를 받아 이미지 업로드 후 썸네일 URL을 반환합니다.
		실패 시 빈 문자열을 반환합니다.
		전제: login2()가 {'NSI': '...'} 형태의 쿠키 dict를 반환.
		hm: {'member_no': ..., 'user_id': ...} 중 하나 포함.
		"""
		url = ""
		try:
			checked_login = self.checkLogin()
			if checked_login == False:
				# 5번 로그인 시도를 했지만 로그인을 하지 못했다.
				# 파서 확인 또는 2차 인증 확인이 필요 (2차 인증도 검증 로직을 추가하자)
				log.printLog("로그인 실패 : 파서 또는 2차 인증 확인 필요")
			else:
				log.printLog("로그인 성공")
				browser = self.driverManager.driver
				browser.get("https://sell.smartstore.naver.com/#/products/bulkadd")

				try:
					for _ in range(1,5):
						res_data = self.apiManager.parsingInsertBulkLink({'cookies':self.getCookies()})
						if res_data:
							break
						time.sleep(0.5)
					res_data_json = json.loads(res_data)
					log.printLog(res_data_json)

					res_thumbnail_data = ""
					res_data_json['img_path'] = file_path
					res_data_json['cookies'] = self.getCookies()
					for _ in range(1,5):
						res_thumbnail_data = self.apiManager.uploadImageToSmartstore(res_data_json)
						if res_thumbnail_data:
							break
						time.sleep(0.5)
					
					log.printLog(res_thumbnail_data)
					# 4) <thumbnail>...</thumbnail> 추출
					m = re.search(r"<thumbnail>(.*?)</thumbnail>", res_thumbnail_data, flags=re.IGNORECASE | re.DOTALL)
					url = ""
					if m:
						url = m.group(1).strip()
					return url
				except Exception as e:
					log.printException(e)
    
				# SE_APP_ID = "SE-ed6e4fa8-32e7-4019-a32a-fbb096148fe5"
				# cookies = self.getCookies()  # 외부 정의: 로그인하여 쿠키(dict) 반환
				# user_id = str(hm.get("member_no") or hm.get("user_id") or "").strip()
				# if not user_id:
				# 	return ""

				# session = requests.Session()
				# session.cookies.update(cookies)

				# # 1) 에디터 토큰 조회
				# auth_url = (
				# 	f"https://sell.smartstore.naver.com/api/v2/editor/auth-token"
				# 	f"?target_appcode=shoppc001&user_id={user_id}"
				# )
				# auth_headers = {
				# 	"Host": "platform.editor.naver.com",
				# 	"Referer": "https://sell.smartstore.naver.com/",
				# 	"Origin": "https://sell.smartstore.naver.com",
				# 	"Sec-Fetch-Site": "same-site",
				# 	"Sec-Fetch-Mode": "cors",
				# 	"Sec-Fetch-Dest": "empty",
				# }
				# auth_res = session.get(auth_url, headers=auth_headers, timeout=60)
				# auth_res.raise_for_status()
				# token_key = auth_res.json().get("token", "")
				# if not token_key:
				# 	return ""

				# # 2) 포토 업로더 세션키 조회
				# sk_url = (
				# 	f"https://platform.editor.naver.com/api/shoppc001/v1/photo-uploader/session-key"
				# 	f"?userId={user_id}"
				# )
				# sk_headers = {
				# 	"Host": "platform.editor.naver.com",
				# 	"Origin": "https://sell.smartstore.naver.com",
				# 	"Sec-Fetch-Site": "same-site",
				# 	"Sec-Fetch-Mode": "cors",
				# 	"Sec-Fetch-Dest": "empty",
				# 	"Referer": "https://sell.smartstore.naver.com/",
				# 	"SE-Authorization": token_key,
				# 	"SE-App-Id": SE_APP_ID,
				# }
				# sk_res = session.get(sk_url, headers=sk_headers, timeout=60)
				# sk_res.raise_for_status()
				# session_key = sk_res.json().get("sessionKey", "")
				# if not session_key:
				# 	return ""

				# # 3) 이미지 업로드
				# upload_url = (
				# 	f"https://ecommerce.upphoto.naver.com/{session_key}/simpleUpload/0"
				# 	f"?userId={user_id}&extractExif=true&extractAnimatedCnt=true&autorotate=true"
				# 	f"&extractDominantColor=false&type=&customQuery="
				# )
				# upload_headers = {
				# 	"Host": "ecommerce.upphoto.naver.com",
				# 	"Connection": "keep-alive",
				# 	"Origin": "https://sell.smartstore.naver.com",
				# 	"Sec-Fetch-Site": "same-site",
				# 	"Sec-Fetch-Mode": "cors",
				# 	"Sec-Fetch-Dest": "empty",
				# 	"Referer": "https://sell.smartstore.naver.com/",
				# 	"Pragma": "no-cache",
				# }

				# file_path_str = str(file_path)
				# with open(file_path_str, "rb") as f:
				# 	files = {"image": (Path(file_path_str).name, f, "application/octet-stream")}
				# 	up_res = session.post(upload_url, headers=upload_headers, files=files, timeout=(30, 30))
				# 	up_res.raise_for_status()
				# 	body = up_res.text

				# # 4) <thumbnail>...</thumbnail> 추출
				# m = re.search(r"<thumbnail>(.*?)</thumbnail>", body, flags=re.IGNORECASE | re.DOTALL)
				# if m:
				# 	url = m.group(1).strip()
		except Exception as e:
			log.printException(e)
		return False
	
	# public static String img_upload(File file, HashMap hm) 
 	# {
	# 	String url = "";

	# 	try { 
    #    		Map cookies = login2();
    
	# 		System.out.println("img cookies:" + cookies);
    # 		Connection.Response res = Jsoup.connect("https://sell.smartstore.naver.com/api/v2/editor/auth-token?target_appcode=shoppc001&user_id=" + common.nvl(userVO.getMember_no())).method(Connection.Method.GET).header("Host", "platform.editor.naver.com").header("Referer", "https://sell.smartstore.naver.com/").header("Origin", "https://sell.smartstore.naver.com").header("Sec-Fetch-Site", "same-site").header("Sec-Fetch-Mode", "cors").header("Sec-Fetch-Dest", "empty").cookies(cookies).timeout(60000).ignoreHttpErrors(true).ignoreContentType(true).execute();
    
    # 		HashMap map = (HashMap)(new ObjectMapper()).readValue(res.body(), HashMap.class);
    # 		String token_key = common.nvl(map.get("token"));

	# 	    Connection.Response res_session = Jsoup.connect("https://platform.editor.naver.com/api/shoppc001/v1/photo-uploader/session-key?userId=" + common.nvl(userVO.getMember_no())).method(Connection.Method.GET).header("Host", "platform.editor.naver.com").header("Origin", "https://sell.smartstore.naver.com").header("Sec-Fetch-Site", "same-site").header("Sec-Fetch-Mode", "cors").header("Sec-Fetch-Dest", "empty").header("Referer", "https://sell.smartstore.naver.com/").header("SE-Authorization", token_key).header("SE-App-Id", "SE-ed6e4fa8-32e7-4019-a32a-fbb096148fe5").cookies(cookies).timeout(60000).ignoreHttpErrors(true).ignoreContentType(true).execute();
		    
	# 	    HashMap session_map = (HashMap)(new ObjectMapper()).readValue(res_session.body(), HashMap.class);
	# 	    String session_key = common.nvl(session_map.get("sessionKey"));
		    
	# 	    HttpPost post = new HttpPost("https://ecommerce.upphoto.naver.com/" + session_key + "/simpleUpload/0?userId=" + common.nvl(userVO.getMember_no()) + "&extractExif=true&extractAnimatedCnt=true&autorotate=true&extractDominantColor=false&type=&customQuery=");
	# 	    post.setHeader("Host", "ecommerce.upphoto.naver.com");
	# 	    post.setHeader("Connection", "keep-alive");
	# 	    post.setHeader("Origin", "https://sell.smartstore.naver.com");
	# 	    post.setHeader("Sec-Fetch-Site", "same-site");
	# 	    post.setHeader("Sec-Fetch-Mode", "cors");
	# 	    post.setHeader("Sec-Fetch-Dest", "empty");
	# 	    post.setHeader("Referer", "https://sell.smartstore.naver.com/");
	# 	    post.setHeader("Cookie", "NSI=" + cookies.get("NSI"));
	# 	    post.setHeader("Pragma", "no-cache");
		    
	# 	    MultipartEntityBuilder meb = MultipartEntityBuilder.create();
	# 	    meb.setMode(HttpMultipartMode.BROWSER_COMPATIBLE);
	# 	    meb.addPart("image", (ContentBody)new FileBody(file));
		    
	# 	    post.setEntity(meb.build());
		    
	# 	    RequestConfig config = RequestConfig.custom().setConnectionRequestTimeout(30000).setSocketTimeout(30000).setConnectTimeout(30000).build();
		    
	# 	    HttpClientBuilder builder = HttpClients.custom().setDefaultRequestConfig(config);
		    
	# 	    CloseableHttpClient client = builder.build();
		    
	# 	    CloseableHttpResponse closeableHttpResponse = client.execute((HttpUriRequest)post);
	# 	    HttpEntity resEntity = closeableHttpResponse.getEntity();
		    
	# 	    String check = EntityUtils.toString(resEntity);
	# 	    String[] arr = check.split("\\<thumbnail\\>");
	# 	    String[] thumbnail = arr[1].split("\\<\\/thumbnail\\>");

	# 	    return url; 
    #   } catch (Exception e) { return url; } finally { Exception exception = null; }

	# }

