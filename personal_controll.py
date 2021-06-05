import os
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QMessageBox

import time
import requests
import json
from flask import request, jsonify

url = 'http://127.0.0.1:5000/'

def changePage(page):
    wiget.setCurrentIndex(page)


class presonalInitialWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI\\personal_init.ui', self)
        self.user_join_BTN.clicked.connect(lambda : changePage(1))
        self.user_login_BTN.clicked.connect(lambda : changePage(2))


class userRegisterWindow(QMainWindow):                                                  ##一般用戶介面
    def __init__(self):
        super().__init__()
        loadUi('UI\\user_register.ui', self)
        self.back_BTN.clicked.connect(lambda : self.clear_and_changePage())
        self.email_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))
        
        self.password_input.setMaxLength(15)
        self.password_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))
        
        self.confirm_password_input.setMaxLength(15)
        self.confirm_password_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.confirm_password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        
        self.school_input.setMaxLength(30)

        self.send_btn.clicked.connect(self.check_psw)
        self.go_login_BTN.clicked.connect(lambda : changePage(2))

    def clear_and_changePage(self):
        changePage(0)
        self.email_input.clear()
        self.confirm_password_input.clear()
        self.school_input.clear()
        


    def check_psw(self):
        if self.email_input.text() == '' or self.password_input.text() == '' or self.confirm_password_input.text() == '' or self.school_input.text() == '':
            self.info_label.setText('請檢察是否有空欄位')
        else:
            if len(self.email_input.text()) <= 5:
                self.info_label.setText('Email格式有誤')
            else:
                if self.email_input.text()[-4:] == '.com' and '@' in self.email_input.text() and self.email_input.text().count('@') ==1 and self.email_input.text()[0] != '@' :
                    if len(self.password_input.text()) >= 6 and len(self.password_input.text()) <=15:
                        if len(self.confirm_password_input.text()) >= 6 and len(self.confirm_password_input.text()) <=15:
                            if self.password_input.text() == self.confirm_password_input.text():
                                reply = QMessageBox.information(self, '信息', '您的註冊已完成，點擊跳轉至登入頁面', QMessageBox.Ok | QMessageBox.Close)
                                
                                # self.register_company_account()       ############call上傳
                                
                                # print(reply)
                                if reply == 1024:
                                    changePage(2)
                                    self.email_input.clear()
                                    self.password_input.clear()
                                    self.confirm_password_input.clear()
                                    self.school_input.clear()
                                    self.info_label.setText('')                       
                                else:
                                    changePage(0)
                            else:
                                self.info_label.setText('兩密碼不一致')
                        else:
                            self.info_label.setText('確認密碼長度錯誤')
                    else:
                        self.info_label.setText('密碼長度錯誤')
                else:
                    self.info_label.setText('Email格式錯誤')

    # def register_company_account(self):
    #     print("register_user_account--------------------")
    #     iscompany = True
    #     send_data = {
    #         "table":"users",
    #         "account": self.email_input.text(),
    #         "password": self.password_input.text(),

    #         "school": self.school_input.text(),                             #####多學校上傳

    #         "iscompany": iscompany}
    #     send_data_json = json.dumps(send_data)
    #     r = requests.post(url + 'add_to_table', json=send_data_json)
                
class userLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI\\user_login.ui', self)
        self.back_BTN.clicked.connect(lambda : changePage(0))
        self.email_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))
        self.password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        self.password_input.setMaxLength(15)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.go_forget_ps_BTN.clicked.connect(lambda : changePage(3))
        self.login_BTN.clicked.connect(self.checkLogin)
        self.go_join_BTN.clicked.connect(lambda : changePage(1))

    def checkLogin(self):       ########################################完成取得資料後寫帳密核對
        changePage(4)

        # # print("check login--------------------")
        # # send_data = {"account":self.email_phone_input.text()}
        # # send_data_json = json.dumps(send_data)

        # # print(send_data_json)
        # # print(type(send_data_json))
        # # r = requests.post(url + 'test', json=send_data_json)
        # # print(r)
        # # print(r.text)

        # iscompany = True
        # print("company_checkLogin--------------------")
        # send_data = {
        #     "account": self.email_phone_input.text(),
        #     "password": self.password_input.text(),
        #     "iscompany":iscompany    }
        # send_data_json = json.dumps(send_data)
        # r = requests.post(url + 'check_password', json=send_data_json)
        # r = json.loads(r.text)
        # print(r)
        # if r["status"] == 'ok':
        #     changePage(4)
        # else:  ########################################錯誤訊息
        #     # TODO
        #     pass

class forgetPSWindow(QMainWindow):    #####other
    def __init__(self):
        super(forgetPSWindow, self).__init__()
        loadUi('UI\\forget_password.ui', self)
        self.back_BTN.clicked.connect(lambda : changePage(0))
        self.email_phone_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))
        self.reset_BTN.clicked.connect(self.check_data_exist)

    def check_data_exist(self):         ##############################確認其資料後，進入更改介面判斷式
        changePage(5)

class changePSWindow(QMainWindow):
    def __init__(self):
        super(changePSWindow, self).__init__()
        loadUi('UI\\change_interface.ui', self)
        self.password_input.setMaxLength(15)
        self.password_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        self.confirm_password_input.setMaxLength(15)
        self.confirm_password_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.confirm_password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        self.finish_BTN.clicked.connect(self.send_reset_data)
        self.back_BTN.clicked.connect(lambda : changePage(0))

    def send_reset_data(self):
        if len(self.password_input.text()) >=6 and len(self.password_input.text()) <= 15:
            if self.password_input.text() == self.confirm_password_input.text():
                reply = QMessageBox.information(self, '信息', '您的密碼重設完成，請重新登入', QMessageBox.Ok)
                # print(reply)
                
                self.password_input.clear()
                self.confirm_password_input.clear()
                self.info_label.setText('')
                changePage(0)

            else:
                self.info_label.setText('兩組密碼不一致')
        else:
            self.info_label.setText('請確定密碼長度正確')     
        
class userResumeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI\\user_resume.ui', self)

        self.phone_input.setMaxLength(10)
        self.phone_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))

        self.age_input.setMaxLength(3)
        self.age_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))

        self.email_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))

        self.salary_input.setMaxLength(12)
        self.salary_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))

        
        # self.loading_data()         #導入初始對應資料(如果有的話)

        self.logout_BTN.clicked.connect(lambda : self.logout_function())
        self.work_search_BTN.clicked.connect(self.search_job)
        self.update_modify_BTN.clicked.connect(self.update_modify)
        self.salary_type_comboBox.currentIndexChanged.connect(self.activate_salary_input)
        self.mail_BTN.clicked.connect(self.go_mail)

    def reset(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.gender_comboBox.setCurrentIndex(0)
        self.age_input.clear()
        self.address_input.clear()
        self.soilder_comboBox.setCurrentIndex(0)
        self.education_comboBox.setCurrentIndex(0)
        self.email_input.clear()
        self.school_input.clear()
        self.department_comboBox.setCurrentIndex(0)
        self.place_comboBox.setCurrentIndex(0)
        self.salary_type_comboBox.setCurrentIndex(0)
        self.salary_input.setEnabled(False)
        self.salary_input.clear()
        self.skill_input.clear()
        self.profile_input.clear()

    def upload_data(self):
        if self.salary_type_comboBox.currentIndex() != 0 and self.salary_input.text() != '':
            if self.salary_type_comboBox.currentIndex() == 1:
                hourSalary = int(self.salary_input.text())
                daySalary = hourSalary * 8
                monthSalary = daySalary * 22
                yearSalary = monthSalary * 12
            elif self.salary_type_comboBox.currentIndex() == 2:
                daySalary = int(self.salary_input.text())
                hourSalary = daySalary // 8
                monthSalary = daySalary * 22
                yearSalary = monthSalary * 12
            elif self.salary_type_comboBox.currentIndex() == 3:
                monthSalary = int(self.salary_input.text())
                yearSalary = monthSalary * 12
                daySalary = monthSalary // 22
                hourSalary = daySalary // 8
            elif self.salary_type_comboBox.currentIndex() == 4:
                yearSalary = int(self.salary_input.text())
                monthSalary = yearSalary // 12
                daySalary = monthSalary // 22
                hourSalary = daySalary // 8
        else:
            self.salary_type_comboBox.setCurrentIndex(0)
            self.salary_input.setEnabled(False)
            hourSalary = ''
            daySalary = ''
            monthSalary = ''
            yearSalary = ''
        
        if self.gender_comboBox.currentText() == '-':
            gender = ''
        else:
            gender = self.gender_comboBox.currentText()
        
        if self.education_comboBox.currentText() == '請選擇':
            education = ''
        else:
            education = self.education_comboBox.currentText()

        if self.department_comboBox.currentText() == '請選擇科系類別':
            department = ''
        else:
            department = self.department_comboBox.currentText()

        if self.place_comboBox.currentText() == '請選擇上班地點':
            place = ''
        else:
            place = self.place_comboBox.currentText()
            
        send_data = {'name' : self.name_input.text(), 'phone' : self.phone_input.text(), 'gender' : gender, 'age' : self.age_input.text(), 'address' : self.address_input.toPlainText(), 'soilder' : self.soilder_comboBox.currentText(), 'education' : education, 'email' : self.email_input.text(), 'school' : self.school_input.text(), 'department' : department, 'place' : place, 'hourSalary' : hourSalary, 'daySalary' : daySalary, 'monthSalary' : monthSalary, 'yearSalary' : yearSalary, 'skill' : self.skill_input.toPlainText(), 'profile' : self.profile_input.toPlainText()}
        print(send_data)

        ######################################################這裡上傳資料

    def leave_page(self):
        if self.name_input.isEnabled() == True:
            reply = QMessageBox.information(self, '提示', '您的履歷表尚未儲存', QMessageBox.Save | QMessageBox.Discard | QMessageBox.Close)
            return reply
        else:
            return -1

    def logout_function(self):
        reply = self.leave_page()
        # print(reply)
        if reply == 2048:
            
            self.upload_data()

            self.reset()
            changePage(0)
        elif reply == 8388608:
            # print('aaaaa')
            changePage(0)           ###不用會卡視窗
            changePage(4)
            # QMessageBox.accept()
        else:
            self.reset()
            changePage(0)
        

    def control_input(self, switch):
        self.name_input.setEnabled(switch)
        self.phone_input.setEnabled(switch)
        self.gender_comboBox.setEnabled(switch)
        self.age_input.setEnabled(switch)
        self.address_input.setEnabled(switch)
        self.soilder_comboBox.setEnabled(switch)
        self.education_comboBox.setEnabled(switch)
        self.email_input.setEnabled(switch)
        self.school_input.setEnabled(switch)
        self.department_comboBox.setEnabled(switch)
        self.place_comboBox.setEnabled(switch)
        self.salary_type_comboBox.setEnabled(switch)
        self.skill_input.setEnabled(switch)
        self.profile_input.setEnabled(switch)

    # def loading_data(self):       ##############################剛進入履歷畫面的資料導入，若有資訊的話
    #     if                                  #####如果導入是有資料的話，預設所有控建為不可用
        # self.control_input(False)
        

    def update_modify(self):
        if self.name_input.isEnabled() == False:
            self.control_input(True)
        else:
            self.upload_data()
            ######################################################上傳資料

            self.control_input(False)

    def activate_salary_input(self):
        if self.salary_type_comboBox.currentIndex() != 0:
            self.salary_input.setEnabled(True)
        else:
            self.salary_input.setEnabled(False)


    def search_job(self):
        reply = self.leave_page()
        if reply == 2048:

            self.upload_data()


            self.reset()
            changePage(6)
        elif reply == 8388608:
            changePage(0)           ###不用會卡視窗
            changePage(4)
        else:
            self.reset()
            changePage(6)

    def go_mail(self):
        reply = self.leave_page()
        if reply == 2048:
            self.upload_data()
            self.reset()
            changePage(8)
        elif reply == 8388608:
            changePage(0)           ###不用會卡視窗
            changePage(4)
        else:
            self.reset()
            changePage(8)
        
class userSearchEngineWindow(QMainWindow):    
    def __init__(self):
        super().__init__()
        loadUi('UI\\user_search_engine.ui', self)
        self.back_BTN.clicked.connect(lambda : changePage(4))
        self.salary_input.setMaxLength(12)
        self.salary_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))
        self.search_BTN.clicked.connect(self.send_search)
        self.salary_type_comboBox.currentIndexChanged.connect(self.activate_salary_input)

    def activate_salary_input(self):
        if self.salary_type_comboBox.currentIndex() != 0:
            self.salary_input.setEnabled(True)
        else:
            self.salary_input.setEnabled(False)

    def reset(self):
        self.keyword_input.clear()
        self.department_comboBox.setCurrentIndex(0)
        self.place_comboBox.setCurrentIndex(0)
        self.salary_type_comboBox.setCurrentIndex(0)
        self.salary_input.setEnabled(False)
        self.salary_input.clear()
        
    def send_search(self):
        if self.department_comboBox.currentText() == '-':
            department = ''
        else:
            department = self.department_comboBox.currentText()
        
        if self.place_comboBox.currentText() == '請選擇上班地點':
            place = ''
        else:
            place =self.place_comboBox.currentText()

        if self.salary_type_comboBox.currentIndex() != 0 and self.salary_input.text() != '':
            if self.salary_type_comboBox.currentIndex() == 1:
                hourSalary = int(self.salary_input.text())
                daySalary = hourSalary * 8
                monthSalary = daySalary * 22
                yearSalary = monthSalary * 12
            elif self.salary_type_comboBox.currentIndex() == 2:
                daySalary = int(self.salary_input.text())
                hourSalary = daySalary // 8
                monthSalary = daySalary * 22
                yearSalary = monthSalary * 12
            elif self.salary_type_comboBox.currentIndex() == 3:
                monthSalary = int(self.salary_input.text())
                yearSalary = monthSalary * 12
                daySalary = monthSalary // 22
                hourSalary = daySalary // 8
            elif self.salary_type_comboBox.currentIndex() == 4:
                yearSalary = int(self.salary_input.text())
                monthSalary = yearSalary // 12
                daySalary = monthSalary // 22
                hourSalary = daySalary // 8
        else:
            self.salary_type_comboBox.setCurrentIndex(0)
            self.salary_input.setEnabled(False)
            hourSalary = ''
            daySalary = ''
            monthSalary = ''
            yearSalary = ''
        
        send_data = {'keyword' : self.keyword_input.text(), 'department' : department, 'place' : place, 'hourSalary' : hourSalary, 'daySalary' : daySalary, 'monthSalary' : monthSalary, 'yearSalary' : yearSalary}
        print(send_data)

        ####################################################################上傳搜尋資料

        changePage(7)
        self.reset()
        

class userSearchWindow(QMainWindow):    
    def __init__(self):
        super().__init__()
        loadUi('UI\\user_search_interface.ui', self)
        self.example_data = []
        self.logout_BTN.clicked.connect(lambda : self.leave_reset(0))
        self.back_BTN.clicked.connect(lambda : self.leave_reset(6))
        self.listWidget.itemClicked.connect(self.go_see_detail)

        self.load_data_show()

    def leave_reset(self, page):
        self.listWidget.clear()
        changePage(page)
    

    def load_data_show(self):
        ################################################################讀取搜尋進listWidget

        self.listWidget.clear()

        self.example_data = [{'company_name' : '慧邦科技', 'job_title' : '軟體工程師', 'post_date' : '2021/01/30'},
                        {'company_name' : '國泰金控', 'job_title' : '軟體工程師', 'post_date' : '2020/11/15'},
                        {'company_name' : '毅山科技', 'job_title' : '軟體工程師', 'post_date' : '2021/09/30'}]

        add_text = []
        for i in range(len(self.example_data)):
            add_text.append(self.example_data[i]['company_name'] +','+ self.example_data[i]['job_title'] + ',' + self.example_data[i]['post_date'])
            self.listWidget.addItem(self.example_data[i]['company_name'] +','+ self.example_data[i]['job_title'] + ',' + self.example_data[i]['post_date'])
        print(add_text)

    def go_see_detail(self):
        print(self.listWidget.currentRow())

        # send_data = self.example_data({'company_name' : self.example_data[self.listWidget.currentRow()]['company_name'], 'job_title' : self.example_data[self.listWidget.currentRow()]['job_title'], 'post_data' : self.example_data[self.listWidget.currentRow()]['post_date']})
        
        ######################################################################################################將點選到的資料上傳

        changePage(9)
        

class userMailWindow(QMainWindow):    
    def __init__(self):
        super().__init__()
        loadUi('UI\\user_mail.ui', self)
        self.logout_BTN.clicked.connect(lambda : changePage(0))
        self.back_BTN.clicked.connect(lambda : changePage(4))
        self.scrollAreaWidgetContents.hide()
        self.get_user_send_result()
        self.get_invite()
        self.send_result_comboBox.currentIndexChanged.connect(self.show_result_detail)
        self.invite_comboBox.currentIndexChanged.connect(self.show_invite_detail)
        # self.accept_BTN.clicked.connect(self.send_accept_request)
        # self.reject_BTN.clicked.connect(self.send_reject_request)

    # def send_accept_request(self):
                            ###################################################################傳送同意結果
        # self.decision_BTN_off()

    # def send_reject_request(self):
                            ###################################################################傳送拒絕結果
        # self.decision_BTN_off()

    def decision_BTN_off(self):
        # if                ####################################################################需要有個判斷是否已經回答過邀約的機制
        self.accept_BTN.setEnabled(False)
        self.reject_BTN.setEnabled(False)
        # else:
        self.accept_BTN.setEnabled(True)
        self.reject_BTN.setEnabled(True)
    
    def show_result_detail(self):
        if self.send_result_comboBox.currentText() == '-':
            self.scrollAreaWidgetContents.hide()
        else:
            self.invite_comboBox.setCurrentIndex(0)
            self.scrollAreaWidgetContents.show()
            self.accept_BTN.hide()
            self.reject_BTN.hide()

    def show_invite_detail(self):
        if self.invite_comboBox.currentText() == '-':
            self.scrollAreaWidgetContents.hide()
        else:
            self.send_result_comboBox.setCurrentIndex(0)
            self.scrollAreaWidgetContents.show()
            self.accept_BTN.show()
            self.reject_BTN.show()
            # self.decision_BTN_off()
        

    def get_user_send_result(self):
        #######################################################################################此處取得投遞資料
        self.send_result_comboBox.addItem('國泰金控，軟體工程師')

    def get_invite(self):
        #######################################################################################此處取得邀請資料
        self.invite_comboBox.addItem('慧邦科技，軟體工程師')

    # def user_send_result(self):


class lookCompanyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI\\user_look_requirement.ui', self)
        self.back_BTN.clicked.connect(self.leave_reset)
        # self.send_resume_BTN.clicked.connect(self.send_resume)
        self.load_data()

    # def send_resume(self):
        ####################################################################送出求職訊息

    def load_data(self):
        ###################################################################接收要顯示的訊息
        example_data = {'job_name' : '軟體工程師', 'post_date' : '2021/01/30', 'job_type' : '工讀', 'phone' : '0223917925', 'applicant' : '6' , 'address' : '台北市中正區', 'place' : '台北市', 'salary' : '40000', 'skill': 'python, java', 'profile' : '你知道的'}
        self.company_name_show.setText(example_data['job_name'])
        self.type_comboBox.setCurrentIndex(self.type_comboBox.findText(example_data['job_type']))
        time_info =  example_data['post_date'].replace('/', '.')
        self.post_dateEdit.setDisplayFormat(time_info)
        self.telephone_input.setText(example_data['phone'])
        self.applicant_show.setText(example_data['applicant'])
        self.address_input.setPlainText(example_data['address'])
        self.place_comboBox.setCurrentIndex(self.place_comboBox.findText(example_data['place']))
        self.salary_type_comboBox.setCurrentIndex(self.type_comboBox.findText(example_data['job_type']))
        self.salary_input.setText(example_data['salary'])
        self.skill_require_input.setPlainText(example_data['skill'])
        self.profile_input.setPlainText(example_data['profile'])
        


    def leave_reset(self):
        self.company_name_show.clear()
        self.type_comboBox.setCurrentIndex(0)
        self.post_dateEdit.setDisplayFormat('1.1.2001')
        self.telephone_input.clear()
        self.applicant_show.setText('0')
        self.address_input.clear()
        self.place_comboBox.setCurrentIndex(0)
        self.salary_type_comboBox.setCurrentIndex(0)
        self.skill_require_input.clear()
        self.profile_input.clear()

        changePage(7)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    wiget = QtWidgets.QStackedWidget()
    addMainWindow = presonalInitialWindow()
    addUserRegisterPage = userRegisterWindow()
    addUserLoginPage = userLoginWindow()
    addForgetPassPage = forgetPSWindow()
    addUserResumePage = userResumeWindow()
    addChangeInterface = changePSWindow()
    addUserSearchEngine = userSearchEngineWindow()
    addUserSearchResult = userSearchWindow()
    addUserMailPage = userMailWindow()
    addLookCompanyInfo = lookCompanyWindow()
	
    wiget.addWidget(addMainWindow)              ###初始頁 0

    wiget.addWidget(addUserRegisterPage)        ###註冊頁 1
    wiget.addWidget(addUserLoginPage)           ###燈入頁 2
    wiget.addWidget(addForgetPassPage)          ###忘記密碼 3
    wiget.addWidget(addUserResumePage)          ###履歷表頁 4
    wiget.addWidget(addChangeInterface)         ###改密碼頁 5
    wiget.addWidget(addUserSearchEngine)        ###搜尋頁  6
    wiget.addWidget(addUserSearchResult)        ###結果頁  7
    wiget.addWidget(addUserMailPage)            ###小郵箱  8
    wiget.addWidget(addLookCompanyInfo)         ###看工作資訊  9

    # wiget.setFixedSize(800,600)

    wiget.show()

    sys.exit(app.exec_())