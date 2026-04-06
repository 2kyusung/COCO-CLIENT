# pip install selenium==4.14.0
# pip install selenium webdriver_manager
# import onnxruntime as ort
# import numpy

# from rembg import remove
# from PIL import Image


import sys
import os
import include.log as log
import json
import time


from parsers.parser_manager import ParserManager
from api.api_manager import ApiManager
from config import ConfigCommon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QCheckBox, QLabel, QPlainTextEdit, QMainWindow, QAction, QDesktopWidget, QLineEdit, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
import datetime
from web_crawler.crawler_manager import CrawlerManager

from web_crawler.webbrowser_client import WebView

class Worker(QThread):
    log_update_signal = pyqtSignal(str)

    def __init__(self, headless):
        try:
            super().__init__()
            self.headless = headless
            self.loop_stop = False
            self.api_manager = ApiManager()
        except Exception as e:
            log.printException(e)

    def stop(self):
        self.loop_stop = True
    
    def sendLog(self, log_str):
        self.log_update_signal.emit(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : " + log_str)

    def run(self):
        self.parser_manager = ParserManager('chrome', self.headless, self)
        user_id = ConfigCommon.getCocoWithPeopleUserInfo('user_id')
        # self.parser_manager = ParserManager('firefox', False)
        counting = 0
        while self.loop_stop == False:
            try:
                # Keyword Word Count Check ==============================================================================================
                res_data = None
                for _ in range(1,5):
                    res_data = self.api_manager.getWordCountCheckList({'user_id':user_id})
                    if res_data:
                        break
                    time.sleep(0.2)
                if res_data:
                    try:
                        res_data = json.loads(res_data)
                        keyword_list = res_data.get('data', [])
                        if len(keyword_list) > 0 :
                            self.sendLog("단어수 체크 리스트를 가져옴 : " + str(len(keyword_list)))
                            res_data = self.parser_manager.checkWordCount(keyword_list)
                            if res_data != None:
                                self.api_manager.updateWordCountCheckList({'user_id':user_id, 'keyword_list':json.dumps(res_data)})
                                self.sendLog("단어수 체크 완료")
                    except json.JSONDecodeError as e:
                        log.printLog(res_data)                        
                        self.sendLog("getWordCountCheckList Json Decoder Error")
                time.sleep(0.2)

                # Combine Title Check ==============================================================================================
                res_data = None
                for _ in range(1,5):
                    res_data = self.api_manager.getCheckTitleList({'user_id':user_id})
                    if res_data:
                        break
                    time.sleep(0.2)
                
                if res_data:
                    try:
                        res_data = json.loads(res_data)
                        keyword_list = res_data.get('data', [])
                        if len(keyword_list) > 0 :
                            self.sendLog("조합 키워드 체크 리스트를 가져옴 : " + str(len(keyword_list)))
                            res_data = self.parser_manager.checkCombineTitle(keyword_list)
                            if res_data != None:
                                self.api_manager.updateCheckTitleList({'user_id':user_id, 'keyword_list':json.dumps(res_data)})
                                self.sendLog("조합 키워드 체크 완료")
                    except json.JSONDecodeError as e:
                        log.printLog(res_data)                        
                        self.sendLog("getCheckTitleList Json Decoder Error")
                time.sleep(0.2)

                # Tag List Check ==============================================================================================
                res_data = None
                for _ in range(1,5):
                    res_data = self.api_manager.getCheckTagList({'user_id':user_id})
                    if res_data:
                        break
                    time.sleep(0.2)
                if res_data:
                    try:
                        res_data = json.loads(res_data)
                        checked_tag_list = []
                        keyword_list = res_data.get('data', [])
                        keyword_count = len(keyword_list)
                        ind = 0
                        if len(keyword_list) > 0:
                            self.sendLog("검사할 Tag 리스트를 가져옴 : " + str(len(keyword_list)))
                            while True:
                                tag_list = keyword_list[:10]
                                ind += len(tag_list)
                                del keyword_list[0:10]
                                if len(tag_list) > 0 :
                                    res_data = self.parser_manager.checkTag(tag_list)
                                    if res_data != None:
                                        checked_tag_list.extend(res_data)
                                self.sendLog(str(ind)+"/"+str(keyword_count)+" : TAG 검사 중...")
                                if len(keyword_list) == 0:
                                    break
                            
                            self.api_manager.updateCheckTagList({'user_id':user_id, 'keyword_list':json.dumps(checked_tag_list)})
                            self.sendLog("Tag 리스트 검사 완료")
                    except json.JSONDecodeError as e:
                        log.printLog(res_data)                        
                        self.sendLog("getCheckTagList Json Decoder Error")
                time.sleep(0.2)

                # Insert Image To Smartstore ==================================================================================
                res_data = None
                for _ in range(1,5):
                    res_data = self.api_manager.getInsertImageToSmartstoreList({'user_id':user_id})
                    if res_data:
                        break
                    time.sleep(0.2)
                if res_data:
                    try:
                        res_data = json.loads(res_data)
                        inserted_image_list = []
                        insert_image_to_smartstore_list = res_data.get('data', [])
                        image_count = len(insert_image_to_smartstore_list)
                        ind = 0
                        if len(insert_image_to_smartstore_list) > 0:
                            self.sendLog("등록할 이미지 리스트를 가져옴 : " + str(image_count))
                            for image_item in insert_image_to_smartstore_list:
                                image_file_path = image_item['img_path']
                                if not os.path.exists(image_file_path):
                                    self.sendLog(f"File not found: {image_file_path}")
                                    inserted_image_list.append({'prod_cd':image_item['prod_cd'], 'img_url':'', 'file_not_found':1})
                                else:
                                    thumbnail_url = self.parser_manager.uploadImage(image_file_path)
                                    if isinstance(thumbnail_url, str):
                                        thumbnail_url = f"http://shop1.phinf.naver.net{thumbnail_url}"
                                        self.sendLog(f"Upload Image: {image_item['prod_cd']}")
                                        inserted_image_list.append({'prod_cd':image_item['prod_cd'], 'img_url':thumbnail_url, 'file_not_found':0})
                                    else:
                                        self.sendLog(f"Upload Image Fail: {image_file_path}")

                            self.api_manager.updateInsertImageToSmartstoreList({'user_id':user_id, 'inserted_image_list':json.dumps(inserted_image_list)})
                            self.sendLog("이미지 등록 완료")
                    except json.JSONDecodeError as e:
                        log.printLog(res_data)                        
                        self.sendLog("getCheckTagList Json Decoder Error")

                time.sleep(1)
                counting += 1
                if counting >= 3600:
                    # 30분에 한번씩 browser를 refresh 한다.
                    self.parser_manager.refresh()
                    time.sleep(2)
                    counting = 0
            except Exception as e:
                log.printException(e)
                self.sendLog(str(e))
                self.sendLog("오류 발생, 브라우져가 종료되었습니다. 중지 후 재실행 하세요.")
                self.parser_manager.quit()
        self.parser_manager.quit()


class UtilWorker(QThread):
    log_update_signal = pyqtSignal(str)

    def __init__(self):
        try:
            super().__init__()
            self.loop_stop = False
            self.api_manager = ApiManager()
        except Exception as e:
            log.printException(e)

    def stop(self):
        self.loop_stop = True
    
    def sendLog(self, log_str):
        self.log_update_signal.emit(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : " + log_str)

    def run(self):
        try:
            coco_id = ConfigCommon.getCocoWithPeopleUserInfo('user_id')
            save_image_path = ""

            res_save_image_path = None
            for _ in range(1,5):
                res_save_image_path = self.api_manager.getImageSavePath({'user_id':coco_id})
                if res_save_image_path:
                    break
                time.sleep(0.2)
            log.printLog(res_save_image_path)
            if res_save_image_path:
                res_save_image_path = json.loads(res_save_image_path)
                save_image_path = res_save_image_path.get('data', {}).get('image_save_path', '')

            if save_image_path:
                if os.path.exists(save_image_path):
                    res_dome_product_list = None
                    for _ in range(1,5):
                        res_dome_product_list = self.api_manager.getDomeProductList({'user_id':coco_id})
                        if res_dome_product_list:
                            break
                        time.sleep(0.2)
                    log.printLog(res_dome_product_list)
                    if res_dome_product_list:
                        res_dome_product_list = json.loads(res_dome_product_list)
                        dome_product_list = res_dome_product_list.get('data', [])
                        if len(dome_product_list) > 0:
                            mk_index = 0
                            mk_total = len(dome_product_list)
                            self.sendLog("생성할 폴더 개수 : " + str(mk_total))
                            self.sendLog("폴더 생성 경로 : " + save_image_path)
                            for selfcode in dome_product_list:
                                mk_index += 1
                                if mk_index % 10 == 0:
                                    self.sendLog(str(mk_index) + "/" + str(mk_total))
                                folder_path = save_image_path + "\\" + selfcode
                                if not os.path.exists(folder_path):
                                    os.makedirs(folder_path)
                            self.sendLog(str(mk_index) + "/" + str(mk_total))
                            self.sendLog("폴더 생성을 완료 했습니다.")
                        else:
                            self.sendLog("이미지 작업 전 단계의 상품이 없습니다.")
                else:
                    self.sendLog("이미지 저장 경로에 접근할 수 없습니다.")

            else:
                self.sendLog("이미지 저장 경로가 설정되어 있지 않습니다.")
        except Exception as e:
            log.printException(e)

class SettingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('설정')
        self.setWindowIcon(QIcon('image\\coco_logo.png'))
        self.setGeometry(400, 400, 400, 350)
        self.setFixedSize(400, 200)

        label1 = QLabel('COCO ID', self)
        label1.move(10, 10)
        label1.resize(150, 50)

        self.le_coco_id = QLineEdit(self)
        self.le_coco_id.move(180, 23)
        self.le_coco_id.resize(200, 25)

        label2 = QLabel('스마트스토어 아이디', self)
        label2.move(10, 50)
        label2.resize(150, 50)

        self.le_smartstore_id = QLineEdit(self)
        self.le_smartstore_id.move(180, 60)
        self.le_smartstore_id.resize(200, 25)

        label3 = QLabel('스마트스토어 비밀번호', self)
        label3.move(10, 90)
        label3.resize(150, 50)

        self.le_smartstore_password = QLineEdit(self)
        self.le_smartstore_password.move(180, 98)
        self.le_smartstore_password.resize(200, 25)

        self.b_test = QPushButton('접속 테스트', self)
        self.b_test.move(30, 140)
        self.b_test.resize(150, 30)
        self.b_test.clicked.connect(self.eventTestBtnClick)

        self.b_save = QPushButton('저장', self)
        self.b_save.move(210, 140)
        self.b_save.resize(150, 30)
        self.b_save.clicked.connect(self.eventSaveBtnClick)
        self.center()
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def loadConfigData(self):
        try:
            file_path = "localization.cnf"
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    content = file.read()
                    config_data = json.loads(content)
                    coco_id = config_data.get('coco_id', '')
                    smartstore_id = config_data.get('smartstore_id', '')
                    smartstore_password = config_data.get('smartstore_password', '')
                    self.le_coco_id.setText(coco_id)
                    self.le_smartstore_id.setText(smartstore_id)
                    self.le_smartstore_password.setText(smartstore_password)
        except Exception as e:
            log.printException(e)

    def eventSaveBtnClick(self):
        try:
            coco_id = self.le_coco_id.text()
            smartstore_id = self.le_smartstore_id.text()
            smartstore_password = self.le_smartstore_password.text()

            ConfigCommon.setCocoWithPeopleUserInfo('user_id', coco_id)
            ConfigCommon.setSmartstoreUserInfo('user_id', smartstore_id)
            ConfigCommon.setSmartstoreUserInfo('password', smartstore_password)
            
            config_data = {
                "coco_id":coco_id,
                "smartstore_id":smartstore_id,
                "smartstore_password":smartstore_password
            }
            file_path = "localization.cnf"
            with open(file_path, "w") as file:
                file.write(json.dumps(config_data))
        except Exception as e:
            log.printException(e)
        self.hide()

    def eventTestBtnClick(self):
        try:
            coco_id = self.le_coco_id.text()
            smartstore_id = self.le_smartstore_id.text()
            smartstore_password = self.le_smartstore_password.text()
            if not coco_id or not smartstore_id or not smartstore_password:
                QMessageBox.warning(self, 'Message', '계정 정보가 입력되지 않았습니다.', QMessageBox.Ok, QMessageBox.Ok)
            else:
                ConfigCommon.setCocoWithPeopleUserInfo('user_id', coco_id)
                ConfigCommon.setSmartstoreUserInfo('user_id', smartstore_id)
                ConfigCommon.setSmartstoreUserInfo('password', smartstore_password)
                
                parser_manager = ParserManager('chrome', False)
                if parser_manager.checkLogin() == True:
                    QMessageBox.information(self, 'Message', '스마트스토어 로그인에 성공했습니다.', QMessageBox.Ok, QMessageBox.Ok)
                else:
                    QMessageBox.warning(self, 'Message', '스마트스토어 로그인에 실패했습니다.', QMessageBox.Ok, QMessageBox.Ok)

                parser_manager.quit()
        except Exception as e:
            log.printException(e)


class COCOClient(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            self.loadConfigData()
            self.crawler_manager = CrawlerManager()
            self.api_manager = ApiManager()
            self.initUI()
            self.log_list = []
        except Exception as e:
            log.printException(e)

    def initUI(self):
        try:
            self.client_version = "v1.1.5"
            self.client_version_number = 6; # 서버 API GET_VERSION과 동일하게 변경 해야함.
            self.setWindowTitle(F"COCO {self.client_version}")
            self.setWindowIcon(QIcon('image\\coco_logo.png'))
            self.setGeometry(0, 0, 400, 450)
            if ConfigCommon.getCrawlerMode():
                self.setFixedSize(1200, 800)
            else:
                self.setFixedSize(400, 320)

            # Menu 파일 
            self.menubar = self.menuBar()
            self.menubar.setNativeMenuBar(False)
            file_menu = self.menubar.addMenu("파일")
            # Menu 파일 > 설정
            self.menu_make_folder = QAction("폴더 생성")     
            file_menu.addAction(self.menu_make_folder)
            self.menu_make_folder.triggered.connect(self.openMakeFolder)
            # Menu 파일 > 
            self.menu_setting = QAction("설정")     
            file_menu.addAction(self.menu_setting)
            self.menu_setting.triggered.connect(self.openSetting)

            # file_menu = self.menubar.addMenu("테스트")

            # # Menu 편집 > 설정
            # self.menu_test1 = QAction("테스트1")     
            # file_menu.addAction(self.menu_test1)
            # self.menu_test1.triggered.connect(self.testRun1)


            # Button
            self.b_start = QPushButton('START', self)
            self.b_start.move(10, 30)
            self.b_start.clicked.connect(self.eventStartBtnClick)

            self.cb_headless = QCheckBox('Headless Browser', self)
            self.cb_headless.move(120, 20)
            self.cb_headless.resize(200, 50)
            # self.cb_headless.toggle()
            self.cb_headless.setEnabled(False)

            self.lbl1 = QLabel('Log Message', self)
            self.lbl1.move(13, 60)
            self.lbl1.resize(100, 30)

            self.lbl_coco_id = QLabel('', self)
            self.lbl_coco_id.move(105, 60)
            self.lbl_coco_id.resize(100, 30)

            self.lbl_smartstore_id = QLabel('', self)
            self.lbl_smartstore_id.move(210, 60)
            self.lbl_smartstore_id.resize(200, 30)

            self.te_log = QPlainTextEdit(self)
            # self.te_log.setAcceptRichText(False)
            self.te_log.move(10, 90)
            if ConfigCommon.getCrawlerMode():
                self.te_log.resize(380, 700)
            else:
                self.te_log.resize(380, 220)
                
            self.te_log.setReadOnly(True)

            self.lbl_coco_id.setText(ConfigCommon.getCocoWithPeopleUserInfo('user_id'))
            self.lbl_smartstore_id.setText(ConfigCommon.getSmartstoreUserInfo('user_id'))
            
            if ConfigCommon.getCrawlerMode():
                self.webview = WebView(self)
                self.webview.move(400, 0)
                self.webview.resize(800, 800)
                self.crawler_manager.setWebView(self.webview)
                self.crawler_manager.start()
            

            res_version = self.api_manager.getVersion();
            if res_version != None:
                if self.client_version_number < int(res_version):
                    QMessageBox.information(self, '업데이트 필요', '최신 버전으로 업데이트 하세요', QMessageBox.Ok, QMessageBox.Ok)

            self.center()
            self.show()
        except Exception as e:
            log.printException(e)
    
    def loadConfigData(self):
        try:
            file_path = "localization.cnf"
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    content = file.read()
                    config_data = json.loads(content)
                    coco_id = config_data.get('coco_id', '')
                    smartstore_id = config_data.get('smartstore_id', '')
                    smartstore_password = config_data.get('smartstore_password', '')
                    crawler_mode = config_data.get('crawler_mode', False)

                    ConfigCommon.setCocoWithPeopleUserInfo('user_id', coco_id)
                    ConfigCommon.setSmartstoreUserInfo('user_id', smartstore_id)
                    ConfigCommon.setSmartstoreUserInfo('password', smartstore_password)
                    ConfigCommon.setCrawlerMode(crawler_mode)
                    
        except Exception as e:
            log.printException(e)

    def checkConfigData(self):
        coco_id = ConfigCommon.getCocoWithPeopleUserInfo('user_id')
        smartstore_id = ConfigCommon.getSmartstoreUserInfo('user_id')
        smartstore_password = ConfigCommon.getSmartstoreUserInfo('password')
        if not coco_id or not smartstore_id or not smartstore_password:
            QMessageBox.warning(self, 'Message', '계정 정보가 설정되지 않았습니다.', QMessageBox.Ok, QMessageBox.Ok)
            return False
        return True

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Menu Action 설정
    def openSetting(self):
        self.setting_window = SettingWindow()
        self.setting_window.show()
        self.setting_window.loadConfigData()

    # Menu Action 폴더 생성
    def openMakeFolder(self):
        try:
            self.util_worker = UtilWorker()
            self.util_worker.log_update_signal.connect(self.updateLog)
            self.util_worker.start()
            log.printLog("openMakeFolder")
        except Exception as e:
            log.printException(e)

    def updateLog(self, log_str):
        self.log_list.insert(0,log_str)
        if len(self.log_list) > 1000:
            self.log_list.pop()
        self.te_log.setPlainText("\n".join(self.log_list))
    
    # Start 버튼 클릭 이벤트
    def eventStartBtnClick(self):
        if self.b_start.text() == "START":
            if self.checkConfigData():
                self.b_start.setText("STOP")
                # self.cb_headless.setEnabled(False)
                is_headless = self.cb_headless.isChecked()
                self.worker = Worker(is_headless)
                self.worker.start()
                self.worker.log_update_signal.connect(self.updateLog)
        else:
            self.b_start.setText("START")
            # self.cb_headless.setEnabled(True)
            self.worker.stop()
            self.worker.quit()
            
    def sendLog(self, log_str):
        try:
            self.updateLog(log_str)
        except Exception as e:
            log.printException(e)
            
    # Menu Test 1
    def testRun1(self):
        try:
            parser_manager = ParserManager('chrome', False, self)
            file_path = r'N:\개인\상품\오너클랜\W0DB52D\W0DB52D_01.jpg'
            # INSERT_YOUR_CODE
            if not os.path.exists(file_path):
                log.printLog(f"File not found: {file_path}")
                self.updateLog(f"File not found: {file_path}")
                return
            
            thumbnail_url = parser_manager.uploadImage(file_path)
            log.printLog(thumbnail_url)
            self.updateLog(thumbnail_url)
        except Exception as e:
            log.printException(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = COCOClient()
    sys.exit(app.exec_())
    # client.run()

# log.printLog(__name__)

# parser_manager = ParserManager('firefox', False)