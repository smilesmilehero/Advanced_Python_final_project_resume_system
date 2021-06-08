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

class companyInitialWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/company_init.ui', self)
        self.company_join_BTN.clicked.connect(lambda :changePage(1))
        self.company_login_BTN.clicked.connect(lambda : changePage(2))


class companyRegisterWindow(QMainWindow):                                               ##公司相關介面
    def __init__(self):
        super().__init__()
        loadUi('UI/company_register.ui', self)
        self.back_BTN.clicked.connect(lambda : self.clear_and_changePage(0))
        self.email_input.setMaxLength(50)
        self.email_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))
        self.password_input.setMaxLength(15)
        self.password_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        self.confirm_password_input.setMaxLength(15)
        self.confirm_password_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.confirm_password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        self.send_btn.clicked.connect(self.check_info)
        self.go_login_BTN.clicked.connect(lambda : self.clear_and_changePage(2))

    def clear_and_changePage(self, page):
        changePage(page)
        self.email_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.info_label.setText('')


    def check_info(self):
        if self.email_input.text() == '' or self.password_input.text() == '' or self.confirm_password_input.text() == '':
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

                                # self.register_company_account()       ################################call上傳

                                # print(reply)
                                if reply == 1024:
                                    self.clear_and_changePage(2)
                                else:
                                    self.clear_and_changePage(0)
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

class companyLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/company_login.ui', self)
        self.back_BTN.clicked.connect(lambda : changePage(0))
        self.email_input.setMaxLength(50)
        self.email_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))
        self.password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        self.password_input.setMaxLength(15)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.go_forget_ps_BTN.clicked.connect(lambda : self.reset_leavePage(3))
        self.login_BTN.clicked.connect(self.checkLogin)
        self.go_join_BTN.clicked.connect(lambda : self.reset_leavePage(1))

    def reset_leavePage(self, page):
        changePage(page)
        self.email_input.clear()
        self.password_input.clear()
        self.info_label.setText('')


    def checkLogin(self):       ########################################完成取得資料後寫帳密核對
        # if  #################################################################帳密相符
        self.reset_leavePage(4)

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
        super().__init__()
        loadUi('UI/forget_password.ui', self)
        self.back_BTN.clicked.connect(lambda : self.reset_leavePage(0))
        self.email_input.setMaxLength(50)
        self.email_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))
        self.reset_BTN.clicked.connect(self.check_data_exist)

    def reset_leavePage(self, page):
        changePage(page)
        self.email_input.clear()
        self.info_label.setText('')

    def check_data_exist(self):         ##############################確認其資料後，進入更改介面
        # if    ######################################################判斷成功後
        reply = QMessageBox.information(self, '信息', '請至註冊信箱查收更改密碼信函', QMessageBox.Ok | QMessageBox.Close)
        self.reset_leavePage(2)
        # else:
        # self.info_label.setText('資料不相符，請確認後再輸入')


class companyInterfaceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/company_interface.ui', self)
        self.logout_BTN.clicked.connect(lambda : self.leavePage_function(0))
        self.job_manage_BTN.clicked.connect(lambda : self.leavePage_function(5))
        self.email_input.setMaxLength(50)
        self.email_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))
        self.employee_input.setMaxLength(50)
        self.employee_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))
        self.update_save_BTN.clicked.connect(self.update_modify)

        # self.loading_data()         #導入初始對應資料(如果有的話)

    # def loading_data(self):       ##############################剛進入履歷畫面的資料導入，若有資訊的話
    #     if                                  #####如果導入是有資料的話，預設所有控建為不可用
        # self.control_input(False)

    def control_input(self, switch):
        self.company_name_input.setEnabled(switch)
        self.address_input.setEnabled(switch)
        self.email_input.setEnabled(switch)
        self.employee_input.setEnabled(switch)
        self.department_comboBox.setEnabled(switch)
        self.profile_input.setEnabled(switch)

    def update_modify(self):
        if self.company_name_input.isEnabled() == False:
            self.control_input(True)
        else:
            self.upload_data()
            ######################################################上傳資料

            self.control_input(False)

    def reset(self):
        self.company_name_input.clear()
        self.address_input.clear()
        self.email_input.clear()
        self.employee_input.clear()
        self.department_comboBox.setCurrentIndex(0)
        self.profile_input.clear()

    def upload_data(self):
        if self.department_comboBox.currentText() == '-':
            department = ''
        else:
            department = self.department_comboBox.currentText()

        send_data = {'name' : self.company_name_input.text(), 'address' : self.address_input.toPlainText(), 'email' : self.email_input.text(), 'employees' : self.employee_input.text(), 'industry' : department, 'description' : self.profile_input.toPlainText()}
        print(send_data)

        ###################################################################################上傳公司介面資料

    def leave_page(self):
        if self.company_name_input.isEnabled() == True:
            reply = QMessageBox.information(self, '提示', '您的履歷表尚未儲存', QMessageBox.Save |QMessageBox.Close)
            return reply
        else:
            return -1

    def leavePage_function(self, page):

        reply = self.leave_page()
        # print(reply)
        if self.company_name_input.text() == '' and page == 5:
            reply = QMessageBox.information(self, '提示', '至少要填寫公司名稱', QMessageBox.Save)
            return

        if reply == 2048 or reply == -1:

            self.upload_data()
            if page == 0:
                self.reset()
            self.control_input(False)
            changePage(page)
        elif reply == 2097152 and page == 5:
            reply = QMessageBox.information(self, '提示', '您必須先寫好公司資訊!', QMessageBox.Save)

class companyJobManagement(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/job_manage_interface.ui', self)

        self.telephone_input.setMaxLength(20)
        self.telephone_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))
        self.salary_input.setMaxLength(20)
        self.salary_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))

        self.back_BTN.clicked.connect(lambda : changePage(4))
        self.logout_BTN.clicked.connect(self.reset_all)
        self.update_save_BTN.clicked.connect(self.update_save)
        self.head_hunter_BTN.clicked.connect(lambda : changePage(6))
        self.add_job_and_manage_comboBox.currentIndexChanged.connect(self.job_want_list)
        self.interviewer_comboBox.currentIndexChanged.connect(self.resume_list)
        self.salary_type_comboBox.currentIndexChanged.connect(self.activate_salary_input)
        self.stackedWidget.hide()

        self.interviewer_comboBox.addItem('只是測試') ##########測試顯示第2頁面

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


    # def loading_data(self):                                           ###########################把下拉式選單已有資料導入


    def activate_salary_input(self):
        if self.salary_type_comboBox.currentIndex() != 0:
            self.salary_input.setEnabled(True)
        else:
            self.salary_input.setEnabled(False)

    def Q_switch(self, switch):
        self.company_name_show.setEnabled(switch)
        self.type_comboBox.setEnabled(switch)
        self.telephone_input.setEnabled(switch)
        self.address_input.setEnabled(switch)
        self.place_comboBox.setEnabled(switch)
        self.salary_type_comboBox.setEnabled(switch)
        self.skill_input_2.setEnabled(switch)
        self.profile_input_2.setEnabled(switch)

    def activate_add_new(self):
        self.stackedWidget.show()
        self.stackedWidget.setCurrentIndex(0)
        self.Q_switch(True)

    def resume_list(self):
        self.add_job_and_manage_comboBox.setCurrentIndex(0)
        if self.interviewer_comboBox.currentText() == '-':
            self.stackedWidget.hide()
        else:
                ######################################################放入對應資料顯示
            self.stackedWidget.show()
            self.stackedWidget.setCurrentIndex(1)

    def job_want_list(self):
        self.interviewer_comboBox.setCurrentIndex(0)
        if self.add_job_and_manage_comboBox.currentText() == '新增工作職缺項目':
            self.activate_add_new()
            self.post_time_show.setText(QtCore.QDate.currentDate().toString(QtCore.Qt.ISODate))
        elif self.add_job_and_manage_comboBox.currentText() == '-':
            self.stackedWidget.hide()

    def update_save(self):
        if self.company_name_show.text() == '' or self.telephone_input.text() == '' or self.address_input.toPlainText() == '' or self.skill_input_2.toPlainText() == '' or self.profile_input_2.toPlainText() == '' or self.place_comboBox.currentIndex() == 0 or self.type_comboBox.currentIndex() == 0:
            reply = QMessageBox.information(self, '提示', '須將表格填寫完全才可儲存!', QMessageBox.Ok | QMessageBox.Close)

            if self.add_job_and_manage_comboBox.count() <= 2:
                reply = QMessageBox.information(self, '提示', '此按鈕需先新增工作表，需要新增嗎?', QMessageBox.Ok | QMessageBox.Close)
                # print(reply)
                if reply == 1024:
                    self.activate_add_new()
                else:
                    pass
        else:

            send_data = {'job_name' : self.company_name_show.text(), 'post_time' : self.post_time_show.text(),
                        'job_type' : self.type_comboBox.currentText(), 'phone' : self.telephone_input.text(), 'address' : self.address_input.toPlainText(), 'place' : self.place_comboBox.currentText(), 'salary_type' : self.salary_type_comboBox.currentText(), 'salary' : self.salary_input.text(), 'skill' : self.skill_input_2.toPlainText(), 'profile' : self.profile_input_2.toPlainText()}

            print(send_data)

            #######################################################################################傳送儲存新資料

            self.add_job_and_manage_comboBox.addItem(send_data['job_name'] + ', ' + send_data['post_time'])  ##添加進列表中


    def reset_all(self):
        self.company_name_show.clear()
        self.type_comboBox.setCurrentIndex(0)
        self.post_time_show.clear()
        self.applicant_show.setText('0')
        self.telephone_input.clear()
        self.address_input.clear()
        self.work_where_comboBox.setCurrentIndex(0)
        self.salary_type_comboBox.setCurrentIndex(0)
        self.want_salary_input.clear()
        self.skill_input_2.clear()
        self.profile_input_2.clear()

        self.name_label.clear()
        self.phone_label.clear()
        self.gender_label.clear()
        self.address_label.clear()
        self.age_label.clear()
        self.soilder_label.clear()
        self.email_label.clear()
        self.school_label.clear()
        self.department_label.clear()
        self.salary_type.clear()
        self.salary_label.clear()
        self.place_label.clear()
        self.skill_label.clear()
        self.profile_label.clear()

        changePage(0)



class companySearchEngineWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/company_search_engine.ui', self)
        self.back_BTN.clicked.connect(lambda : self.reset_leavePage(5))
        self.search_BTN.setStyleSheet("QPushButton{border-image: url(UI/magnifying_glass.png)}")
        self.search_BTN.clicked.connect(self.search_go)

    def reset_leavePage(self, page):
        self.keyword_input.clear()
        self.soilder_comboBox.setCurrentIndex(0)
        self.place_comboBox.setCurrentIndex(0)
        self.education_comboBox.setCurrentIndex(0)
        self.salary_type_comboBox.setCurrentIndex(0)
        self.salary_input.setEnabled(False)
        self.salary_input.clear()
        changePage(page)

    def activate_salary_input(self):
        if self.salary_type_comboBox.currentIndex() != 0:
            self.salary_input.setEnabled(True)
        else:
            self.salary_input.setEnabled(False)

    def search_go(self):
        if self.place_comboBox.currentText() == '請選擇上班地點':
            place = ''
        else:
            place = self.place_comboBox.currentText()

        if self.education_comboBox.currentText() == '請選擇':
            education = ''
        else:
            education = self.education_comboBox.currentText()

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

        send_data = {'keyword' : self.keyword_input.text(), 'place' : place, 'education': education, 'hourSalary' : hourSalary, 'daySalary' : daySalary, 'monthSalary' : monthSalary, 'yearSalary' : yearSalary}
        print(send_data)

        ####################################################################上傳搜尋資料

        self.reset_leavePage(7)

class companySearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/company_search_result.ui', self)

        self.logout_BTN.clicked.connect(lambda : self.leave_reset(0))
        self.back_BTN.clicked.connect(lambda : self.leave_reset(6))
        self.listWidget.itemClicked.connect(self.go_see_detail)

        self.load_data_show()

    #################################################################################需在進此頁面前觸發導入結果資料的function

    def leave_reset(self, page):
        self.listWidget.clear()
        changePage(page)


    def load_data_show(self):
        ################################################################讀取搜尋進listWidget

        self.listWidget.clear()

        self.example_data = [{'name' : '陳大名', 'year' : '26', 'school' : '國立台北科技大學', 'department' : '機械工程系',
                             'education' : '學士'},]

        add_text = []
        for i in range(len(self.example_data)):
            add_text.append(self.example_data[i]['name'] +','+ self.example_data[i]['year'] + ',' + self.example_data[i]['school'] + ',' + self.example_data[i]['department'] +','+ self.example_data[i]['education'])
            self.listWidget.addItem(self.example_data[i]['name'] +','+ self.example_data[i]['year'] + ',' + self.example_data[i]['school'] + ',' + self.example_data[i]['department'] +','+ self.example_data[i]['education'])
        print(add_text)

    def go_see_detail(self):
        # print(self.listWidget.currentRow())

        # send_data = self.example_data({'company_name' : self.example_data[self.listWidget.currentRow()]['company_name'], 'job_title' : self.example_data[self.listWidget.currentRow()]['job_title'], 'post_data' : self.example_data[self.listWidget.currentRow()]['post_date']})

        #####################################################################################################將點選到的資料上傳

        changePage(8)

class lookResumeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/company_look_resume.ui', self)
        self.back_BTN.clicked.connect(lambda : self.leave_reset(7))
        self.send_resume_BTN.clicked.connect(self.send_invite)
        self.loading_data()

    # def send_resume(self):
        ####################################################################送出求職訊息

    def loading_data(self):

        ###################################################################接收要顯示的訊息

        example_data = {'name' : '王小琪', 'phone' : '0978996135', 'gender' : '女', 'address' : '嘉義縣太保市', 'age' : '30', 'soilder' : '不提供', 'email' : 'siaoba@gmail.com', 'education' : '博士', 'school' : '國立中央大學', 'department' : '化工所', 'salary_type' : '月薪', 'salary' : '50000', 'place' : '台南市', 'skill': '須具備python, java基礎', 'profile' : '招9晚6，中間休2小'}

        self.name_show.setText(example_data['name'])
        self.phone_show.setText(example_data['phone'])
        self.gender_show.setText(example_data['gender'])
        self.age_show.setText(example_data['age'])
        self.address_show.setText(example_data['address'])
        self.soilder_show.setText(example_data['soilder'])
        self.email_show.setText(example_data['email'])
        self.educatioin_show.setText(example_data['education'])
        self.school_show.setText(example_data['school'])
        self.department_show.setText(example_data['department'])
        self.salary_type_show.setText(example_data['salary_type'])
        self.salary_show.setText(example_data['salary'])
        self.place_show.setText(example_data['place'])
        self.skill_show.setText(example_data['skill'])
        self.profile_show.setText(example_data['profile'])

    def send_invite(self):
        ###########################################################################送出面試邀約

        #########################################################################避免重複投同項工作?

        reply = QMessageBox.information(self, '提示', '成功發送邀約，請耐心等待對方回應', QMessageBox.Ok | QMessageBox.Close)

    def leave_reset(self, page):
        self.name_show.clear()
        self.phone_show.clear()
        self.gender_show.clear()
        self.age_show.clear()
        self.address_show.clear()
        self.soilder_show.clear()
        self.email_show.clear()
        self.educatioin_show.clear()
        self.school_show.clear()
        self.department_show.clear()
        self.salary_type_show.clear()
        self.salary_show.clear()
        self.place_show.clear()
        self.skill_show.clear()
        self.profile_show.clear()

        changePage(page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wiget = QtWidgets.QStackedWidget()
    addMainWindow = companyInitialWindow()
    addCompanyRegisterPage = companyRegisterWindow()
    addCompanyLoginPage = companyLoginWindow()
    addforgetPSWindow = forgetPSWindow()
    addCompanyInterface = companyInterfaceWindow()
    addJobManagement = companyJobManagement()
    addCompanySearchEngine = companySearchEngineWindow()
    addSearchPeople = companySearchWindow()
    addLookResume = lookResumeWindow()

    wiget.addWidget(addMainWindow)                  #初始頁 0
    wiget.addWidget(addCompanyRegisterPage)         #註冊頁 1
    wiget.addWidget(addCompanyLoginPage)            #登入頁 2
    wiget.addWidget(addforgetPSWindow)              #忘記密碼 3
    wiget.addWidget(addCompanyInterface)            #公司主畫面 4
    wiget.addWidget(addJobManagement)               #管理頁 5
    wiget.addWidget(addCompanySearchEngine)         #搜尋引擎 6
    wiget.addWidget(addSearchPeople)                #搜尋結果 7
    wiget.addWidget(addLookResume)                  #看履歷頁 8

    wiget.setMinimumSize(800, 600)
    wiget.show()

    sys.exit(app.exec_())