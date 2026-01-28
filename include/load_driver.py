from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import include.log as log

class DriverManager:
    def __init__(self, browser_name, headless):
        self.driver = None
        self.webdriverLoader(browser_name, headless)

    def webdriverLoader(self, browser_name, headless):
        if browser_name == "chrome" :
            try:
                options = webdriver.ChromeOptions()
                if headless:
                    options.add_argument("headless")
                # mobile_emulation = { "deviceName": "iPhone 12 Pro" }
                # options.add_experimental_option("mobileEmulation", mobile_emulation)
                options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")
                # options.add_argument('--disable-dev-shm-usage')
                # options.add_argument('--log-level=3')
                options.add_argument("start-maximized")
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                # options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option("useAutomationExtension", False)
                # service = Service(executable_path=ChromeDriverManager().install())
                # service = Service(executable_path="D:\\Project\\COCO\\coco-client\\chromedriver\\chromedriver.exe")
                service = Service(executable_path="chromedriver.exe")
                self.driver = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                log.printException(e)
        elif browser_name == "firefox" :        
            try:
                options = webdriver.FirefoxOptions()
                # options.set_headless(headless=headless)
                # options.add_argument('window-size=1920x1080')
                # options.add_argument("disable-gpu")
                options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
                # options.add_argument("lang=ko_KR") # 한국어!
                
                # options.add_argument('lang=en_US')

                profile = webdriver.FirefoxProfile()
                # profile.set_preference("network.proxy.type", 1)
                # profile.set_preference("network.proxy.socks", ConfigCommon.PROXY_INFO.get('socks').get('address'))
                # profile.set_preference("network.proxy.socks_port", ConfigCommon.PROXY_INFO.get('socks').get('port'))
                # profile.set_preference("intl.accept_languages","kr")
                profile.set_preference("permissions.default.desktop-notification",2)
                # 
                # http://kb.mozillazine.org/Category:Preferences
                service = Service(executable_path=GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=options)
                self.driver.set_window_size(1280,1024)
            except Exception as e:
                log.printException(e)

    def stop(self):
        self.driver.quit()