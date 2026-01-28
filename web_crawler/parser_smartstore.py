import time
import include.log as log
import json
from urllib import parse as url_parser
from web_crawler.common_parser import CommonParser, CrawlingState
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineScript
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSignal

class ParserSmartstore(CommonParser):
    def __init__(self, job_data, crawler_manager):
        super().__init__(job_data, crawler_manager)        
    
    def getNextData(self):
        script = """(function() {return JSON.stringify(window.__PRELOADED_STATE__.product.A.seoInfo.sellerTags);})()"""
        return script
    
    def getNextPageURL(self):
        return self.getJobData().mall_url
    
    def getStartURL(self):
        return "https://www.naver.com"

    def nextDataCallback(self, result):
        if result:
            log.printLog(result)
            self.setStatus(CrawlingState.FINISHED)
        else:
            log.printLog("No result")
            self.crawler_manager.addWaitingTime(10) # 크롤링이 실패하면 대기시간을 10초 추가한다.
            self.setStatus(CrawlingState.ERROR)

    
    def parse(self, web_view):
        load_url = web_view.url().toString()
        log.printLog(load_url)
        if load_url.find("www.naver.com"):
            time.sleep(1)
            next_url = self.getNextPageURL()
            # self.webview.load(QUrl(next_url))
            self.crawler_manager.webview_load_url.emit(next_url)
        elif load_url.find("smartstore.naver.com") or load_url.find("brand.naver.com"):
            web_view.page().runJavaScript(self.getNextData(), self.nextDataCallback)

        return []