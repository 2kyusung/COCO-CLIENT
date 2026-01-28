import include.log as log
import time
import json
from urllib import parse as url_parser
from web_crawler.common_parser import CommonParser, CrawlingState
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineScript
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSignal

class ParserNaver(CommonParser):
    def __init__(self, job_data, crawler_manager):
        super().__init__(job_data, crawler_manager)
        self.total_count = 0
        if job_data.target == "keyword_retry":
            self.current_page = job_data.page

    def getStartURL(self):
        url = ""
        keyword = self.getJobData().keyword
        encoded_keyword = url_parser.quote(keyword)

        if self.getJobData().target == "keyword":
            url = "https://msearch.shopping.naver.com/search/all?query=" + encoded_keyword + "&fo=true&frm=NVSHSRC&vertical=home"
        elif self.getJobData().target == "keyword_retry":
            url = self.getNextPageURL()
        elif self.getJobData().target == "keyword_tag":
            url = "https://msearch.shopping.naver.com/search/all?adQuery=" + encoded_keyword + "&fo=true&frm=NVSHSRC&origQuery=" + encoded_keyword + "&pagingIndex=1&pagingSize=40&productSet=checkout&query=" + encoded_keyword + "&sort=rel&viewType=list"            
        return url
    
    def getNextPageURL(self):
        keyword = self.getJobData().keyword
        encoded_keyword = url_parser.quote(keyword)
        next_url = "https://msearch.shopping.naver.com/search/all?adQuery=" + encoded_keyword + "&fo=true&frm=NVSHSRC&origQuery=" + encoded_keyword + "&pagingIndex=" + str(self.current_page) + "&pagingSize=40&productSet=total&query=" + encoded_keyword + "&sort=rel&viewType=list"
        return next_url
    
    def getNextData(self):
        script = """(function() {const nextDataScript = document.getElementById('__NEXT_DATA__');
                    // script 태그 안의 내용을 가져오기 (JSON 문자열로 저장되어 있을 가능성이 큼)
                    var nextDataContent = '';
                    if (nextDataScript) {
                        nextDataContent = nextDataScript.textContent || nextDataScript.innerText;
                    };
                    return nextDataContent; })()"""
        return script
    
    def startCrawling(self, next_url):
        self.webview.load(QUrl(next_url))

    def nextDataCallback(self, result):
        if result:
            next_data = json.loads(result)
            initial_state = next_data.get('props', {}).get('pageProps', {}).get('initialState', None)
            if initial_state:
                initial_state_json = json.loads(initial_state)
                total_count = initial_state_json.get('compositeProducts', {}).get('total', 0)
                self.total_page = total_count // 40 + 1

                if self.getJobData().target == "keyword" and self.current_page < self.total_page and self.current_page < 4:
                    params = {'client_id':self.client_id, 'page':self.current_page, 'next_data':result, 'keyword':self.getJobData().keyword, 'seq':self.getJobData().seq, 'user_id':self.getJobData().user_id, 'status':1, 'target':self.getJobData().target}
                    self.api_manager.sendKeywordPageList(params)
                    time.sleep(2)
                    self.current_page += 1
                    next_url = self.getNextPageURL()
                    # self.webview.load(QUrl(next_url))
                    self.crawler_manager.webview_load_url.emit(next_url)
                else:
                    params = {'client_id':self.client_id, 'page':self.current_page, 'next_data':result, 'keyword':self.getJobData().keyword, 'seq':self.getJobData().seq, 'user_id':self.getJobData().user_id, 'status':2, 'target':self.getJobData().target}
                    self.api_manager.sendKeywordPageList(params)
                    self.setStatus(CrawlingState.FINISHED)
                    self.crawler_manager.resetWaitingTime() # 크롤링이 끝나면 대기시간을 초기화한다.
        else:
            params = {'client_id':self.client_id, 'user_id':self.getJobData().user_id, 'keyword':self.getJobData().keyword, 'page':self.current_page, 'seq':self.getJobData().seq, 'target':self.getJobData().target, 'status':-1}
            self.crawler_manager.addWaitingTime(10) # 크롤링이 실패하면 대기시간을 10초 추가한다.
            self.setStatus(CrawlingState.ERROR)

    def parse(self, web_view):
        log.printLog("ParserNaver Parsing")
        web_view.page().runJavaScript(self.getNextData(), self.nextDataCallback)        
        
        return []