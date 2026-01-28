from dataclasses import dataclass
from api.api_manager import ApiManager
from datetime import datetime

@dataclass
class JobProduct:
    site: str
    target: str
    page: int
    keyword: str
    seq: int
    user_id: str
    mall_url: str

class CrawlingState:
    READY = "READY"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    FINISHED = "FINISHED"
    ERROR = "ERROR"

class CommonParser:
    client_id = "pc_client"

    def __init__(self, job_data, crawler_manager):
        self.job_data = job_data
        self.crawler_manager = crawler_manager
        self.current_page = 1
        self.total_page = -1
        self.crawling_status = CrawlingState.READY
        self.api_manager = ApiManager()
        self.last_request_time = 0

    def getStatus(self):
        return self.crawling_status
    
    def setStatus(self, status):
        self.crawling_status = status

    def getJobData(self):
        return self.job_data

    def getStartURL(self):
        return ""
    
    def getNextPageURL(self):
        return ""

    def parse(self, web_view):
        return None
    
    def setLastRequestTime(self):
        self.last_request_time = datetime.now()
    
    def getDifferenceTime(self):
        return (datetime.now() - self.last_request_time).total_seconds()