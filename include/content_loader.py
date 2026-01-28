import requests
import include.log as log
# from config import ConfigCommon

class ContentLoader:
	
	last_url = ''

	@classmethod
	def getLastUrl(self):
		return self.last_url

	## Keyword Arguments : 
	# 		headers : Request Header List, Key Value의 Map Type
	#		user_agent : String, Headers에서 설정할 수 있으며, 몇시적으로 지정할 수도 있다. User Agent가 설정되지 않을 경우 Default User Agent가 설정된다.
	# 		cookies : Request Cookies
	# Parameters:	
	# method – method for the new Request object.
	# url – URL for the new Request object.
	# params – (optional) Dictionary, list of tuples or bytes to send in the query string for the Request.
	# data – (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body of the Request.
	# json – (optional) A JSON serializable Python object to send in the body of the Request.
	# headers – (optional) Dictionary of HTTP Headers to send with the Request.
	# cookies – (optional) Dict or CookieJar object to send with the Request.
	# files – (optional) Dictionary of 'name': file-like-objects (or {'name': file-tuple}) for multipart encoding upload. file-tuple can be a 2-tuple ('filename', fileobj), 3-tuple ('filename', fileobj, 'content_type') or a 4-tuple ('filename', fileobj, 'content_type', custom_headers), where 'content-type' is a string defining the content type of the given file and custom_headers a dict-like object containing additional headers to add for the file.
	# auth – (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
	# timeout (float or tuple) – (optional) How many seconds to wait for the server to send data before giving up, as a float, or a (connect timeout, read timeout) tuple.
	# allow_redirects (bool) – (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to True.
	# proxies – (optional) Dictionary mapping protocol to the URL of the proxy.
	# verify – (optional) Either a boolean, in which case it controls whether we verify the server’s TLS certificate, or a string, in which case it must be a path to a CA bundle to use. Defaults to True.
	# stream – (optional) if False, the response content will be immediately downloaded.
	# cert – (optional) if String, path to ssl client cert file (.pem). If Tuple, (‘cert’, ‘key’) pair.
	@classmethod
	def getContent(self, url, **kargs):
		try:
			headers = kargs.get('headers', {})
			user_agent = kargs.get('user_agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")
			
			if user_agent != None:
				headers['User-Agent'] = user_agent

			if headers.get('Accept', None) == None and headers.get('accept', None) == None:
				headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'

			if headers.get('user_agent', None) == None and headers.get('User_Agent', None) == None:
				headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'  # DESCTOP의 chrome version의 User Agent를 입력한다.
			
			referer = kargs.get('referer', None)
			if referer != None:
				headers['Referer'] = referer			

			cookies = kargs.get('cookies', None)

			timeout = kargs.get('timeout', (5, 15))

			allow_redirects = kargs.get('allow_redirects', True)

			method = kargs.get('method', 'GET')
   
			files = kargs.get('files', None)

			postdata = kargs.get('postdata', None)
			data_type = kargs.get('data_type', None)
			json_data = None		
			if data_type == "json" and postdata != None:
				json_data = postdata
				postdata = None

			return_error_code = kargs.get('return_error_code', False)

			# proxy = None
			use_proxy = kargs.get('use_proxy', False)
			proxy = kargs.get('proxy', None)
			# if use_proxy:  # Server에서 통신할 경우는 Proxy를 사용하지 않기 위해, Default는 사용.
			# 	proxy_socks = ConfigCommon.PROXY_INFO.get('socks', None)
			# 	if proxy_socks:
			# 		proxy_address = proxy_socks.get('address')
			# 		proxy_port = proxy_socks.get('port')
			# 		proxy = {'http':proxy_address + ':' + str(proxy_port), 'https':proxy_address + ':' + str(proxy_port)}
		except Exception as e:
			log.printException(e)		
		try:
			self.last_url = url
			# log.printLog(url)
			if method.upper() == "GET":
				response = requests.get(url, headers=headers, cookies=cookies, timeout=timeout, allow_redirects=allow_redirects, proxies=proxy)
			elif method.upper() == "POST":
				response = requests.post(url, headers=headers, cookies=cookies, timeout=timeout, allow_redirects=allow_redirects, proxies=proxy, data=postdata, json=json_data, files=files)
				# log.printLog("Method POST")
				# log.printLog("URL : " + url)
				# log.printLog(postdata)
				# log.printLog(json_data)
			elif method.upper() == "PUT":
				# log.printLog("Method PUT")
				# log.printLog("URL : " + url)
				# log.printLog(postdata)
				# log.printLog(json_data)
				response = requests.put(url, headers=headers, cookies=cookies, timeout=timeout, allow_redirects=allow_redirects, proxies=proxy, data=postdata, json=json_data)
			elif method.upper() == "DELETE":
				response = requests.delete(url, headers=headers, cookies=cookies, timeout=timeout, allow_redirects=allow_redirects, proxies=proxy)
			else:
				response = requests.get(url, headers=headers, cookies=cookies, timeout=timeout, allow_redirects=allow_redirects, proxies=proxy)

			# log.printLog(response)
			if response.status_code == 200 or response.status_code == 201:
				return response
			else:
				if return_error_code:
					return response
				else:
					log.printLog(response.status_code)
					log.printLog(response.text)
					return response

		except Exception as e:
			log.printException(e)
		
		# Exceptions
		# exception requests.RequestException(*args, **kwargs)[source]
		# There was an ambiguous exception that occurred while handling your request.

		# exception requests.ConnectionError(*args, **kwargs)[source]
		# A Connection error occurred.

		# exception requests.HTTPError(*args, **kwargs)[source]
		# An HTTP error occurred.

		# exception requests.URLRequired(*args, **kwargs)[source]
		# A valid URL is required to make a request.

		# exception requests.TooManyRedirects(*args, **kwargs)[source]
		# Too many redirects.

		# exception requests.ConnectTimeout(*args, **kwargs)[source]
		# The request timed out while trying to connect to the remote server.

		# Requests that produced this error are safe to retry.

		# exception requests.ReadTimeout(*args, **kwargs)[source]
		# The server did not send any data in the allotted amount of time.

		# exception requests.Timeout(*args, **kwargs)[source]
		# The request timed out.

		# Catching this error will catch both ConnectTimeout and ReadTimeout errors.

		return None