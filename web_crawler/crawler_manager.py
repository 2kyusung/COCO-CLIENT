import time
import json

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import QUrl

import include.log as log
from api.api_manager import ApiManager
from web_crawler.common_parser import CrawlingState, JobProduct, CommonParser
from web_crawler.parser_naver import ParserNaver
from web_crawler.parser_smartstore import ParserSmartstore



class CrawlerManager(QThread):
    webview_start_crawling = pyqtSignal()
    webview_load_url = pyqtSignal(str)
    def __init__(self):
        try:
            super().__init__()
            self.stop_crawler = False
            self.webview = None
            self.api_manager = ApiManager()
            self.parser = None
            self.waiting_time = 10 # 10초
            self.job_list = []
        except Exception as e:
            log.printException(e)

    def addWaitingTime(self, time): # 오류가 발생 했을 경우 Waiting Time을 추가한다.
        self.waiting_time += time

    def resetWaitingTime(self): # Waiting Time을 초기화 한다.
        self.waiting_time = 10

    def setWebView(self, webview):
        try:
            log.printLog("setWebView")
            log.printLog(webview)
            self.webview = webview

            self.webview_start_crawling.connect(self.startCrawling)
            self.webview_load_url.connect(self.loadNextPage)
            self.webview.loadStarted.connect(self.loadStarted)
            self.webview.loadFinished.connect(self.loadFinished)
            
        except Exception as e:
            log.printException(e)    

    def startCrawling(self):
        try:
            start_url = self.parser.getStartURL()
            log.printLog(start_url)
            if start_url != None:
                self.parser.setStatus(CrawlingState.RUNNING)
                self.parser.setLastRequestTime()
                self.webview.load(QUrl(start_url))
                self.webview.show()
        except Exception as e:
            log.printException(e)

    def loadNextPage(self, next_url):
        try:
            log.printLog(next_url)
            if next_url != None:
                self.parser.setStatus(CrawlingState.RUNNING)
                self.parser.setLastRequestTime()
                self.webview.load(QUrl(next_url))
            else:
                self.parser.setStatus(CrawlingState.ERROR)
                # self.webview.show()
        except Exception as e:
            log.printException(e)


    def loadStarted(self):
        try:
            log.printLog("Load Started")
        except Exception as e:
            log.printException(e)

    def loadFinished(self, result):
        try:
            log.printLog("Load Finished")
            if result == False:
                log.printLog("Load Failed")
                self.parser.setStatus(CrawlingState.ERROR)
            else:
                log.printLog("Load Success")
                self.parser.parse(self.webview)
            
        except Exception as e:
            log.printException(e)

    def cvtJobItem(self, product):
        site = product.get("site", "")
        target = product.get("target", "")
        page = product.get("page", -1)
        keyword = product.get("keyword", "")
        seq = product.get("seq", 0)
        user_id = product.get("user_id", "")
        mall_url = product.get("mall_url", "")
        if site == "" or target == "":
            return None
        return JobProduct(site, target, page, keyword, seq, user_id, mall_url)
    
    # 크롤링할 목록을 가져온다.
    def getCrawlingItemList(self):
        try:
            log.printLog(self.parser)
            params = {'client_id':CommonParser.client_id, 'size':1, 'debug':0}
            res_data = self.api_manager.getCrawlingItemList(params)
            if res_data:
                res_data = json.loads(res_data)
                log.printLog(res_data)
                result_status = res_data.get("status", False)
                if result_status == True:
                    product_list = res_data.get("data", [])
                    data_size = res_data.get("data_size", 0)
                    for product in product_list:
                        job_data = self.cvtJobItem(product)
                        if job_data != None:
                            log.printLog(job_data)
                            self.job_list.append(job_data)
        except Exception as e:
            log.printException(e)
            return None
    
    def getParser(self, job_data):
        try:
            log.printLog(job_data)
            if job_data.site == "naver":
                log.printLog("naver parser")
                return ParserNaver(job_data, self)
            elif job_data.site == "smartstore":
                return ParserSmartstore(job_data, self)
        except Exception as e:
            log.printException(e)

    # Site와 Target에 맞는 크롤링을 시작한다.
    def crawlingStart(self):
        try:
            if len(self.job_list) > 0:
                job_data = self.job_list.pop(0)
                
                site = job_data.site
                target = job_data.target
                if site == "" or target == "":
                    return None
                self.parser = self.getParser(job_data)
                self.webview_start_crawling.emit()
        except Exception as e:
            log.printException(e)
            return None
        
    def waitingCrawlingDone(self):
        try:
            while self.parser != None:                
                if self.parser.getStatus() == CrawlingState.FINISHED or self.parser.getStatus() == CrawlingState.ERROR:
                    break
                time.sleep(0.5)
                # Status가 RUNNING, READY, PAUSED, STOPPED인 경우에는 계속 대기
                # 마지막 Request를 보낸 후 10초이 지나도록 RUNNING 상태가 유지되면 ERROR로 처리
                # if self.parser.getStatus() == CrawlingState.RUNNING:
                diff_time = self.parser.getDifferenceTime()
                if diff_time > 10:
                    self.parser.setStatus(CrawlingState.ERROR)

        except Exception as e:
            log.printException(e)

    def run(self):
        try:
            while self.stop_crawler == False:
                self.getCrawlingItemList() # 서버로부터 크롤링할 목록을 가져옴
                self.crawlingStart()
                self.waitingCrawlingDone()
                self.parser.setStatus(CrawlingState.READY)
                time.sleep(10) # 0.3초 대기
        except Exception as e:
            log.printException(e)