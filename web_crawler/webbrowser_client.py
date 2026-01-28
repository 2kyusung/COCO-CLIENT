import include.log as log
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class WebView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setProduct(self, parser):
        self.parser = parser
        
    def setParser(self, parser):
        self.parser = parser

    def startCrawling(self):
        start_url = self.parser.getStartURL()
        log.printLog(start_url)
        if start_url != None:
            self.load(QUrl(start_url))
            self.show()