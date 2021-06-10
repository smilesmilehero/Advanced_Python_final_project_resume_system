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


user_id = None
isCompany = True


class companyInitialWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/company_init.ui', self)
        self.company_join_BTN.clicked.connect(lambda: changePage(1))
        self.company_login_BTN.clicked.connect(lambda: changePage(2))


class companyRegisterWindow(QMainWindow):  ##公司相關介面
    def __init__(self):
        super().__init__()
        loadUi('UI/company_register.ui', self)
        self.back_BTN.clicked.connect(lambda: self.clear_and_changePage(0))
        self.email_input.setMaxLength(50)
        self.email_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))
        self.password_input.setMaxLength(15)
        self.password_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        self.confirm_password_input.setMaxLength(15)
        self.confirm_password_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.confirm_password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        self.send_btn.clicked.connect(self.check_info)
        self.go_login_BTN.clicked.connect(lambda: self.clear_and_changePage(2))

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
                if self.email_input.text()[
                   -4:] == '.com' and '@' in self.email_input.text() and self.email_input.text().count('@') == 1 and \
                        self.email_input.text()[0] != '@':
                    if len(self.password_input.text()) >= 6 and len(self.password_input.text()) <= 15:
                        if len(self.confirm_password_input.text()) >= 6 and len(
                                self.confirm_password_input.text()) <= 15:
                            if self.password_input.text() == self.confirm_password_input.text():
                                rsp = self.register_company_account()  ############call上傳
                                if rsp == 'err':
                                    self.info_label.setText('帳號已被使用')
                                else:
                                    self.create_company()
                                    reply = QMessageBox.information(self, '信息', '您的註冊已完成，點擊跳轉至登入頁面',
                                                                    QMessageBox.Ok | QMessageBox.Close)
                                    if reply == 1024:
                                        self.clear_and_changePage(2)
                                        self.email_input.clear()
                                        self.password_input.clear()
                                        self.confirm_password_input.clear()
                                        # self.school_input.clear()
                                        self.info_label.setText('')
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

    def register_company_account(self):
        print("register_user_account--------------------")
        send_data = {
            "table": "users",
            "account": self.email_input.text(),
            "password": self.password_input.text(),
            "iscompany": isCompany}
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'add_to_table', json=send_data_json)
        r = json.loads(r.text)
        return r['status']

    def create_company(self):
        send_data = {
            "table": "users",
            "account": self.email_input.text()
        }
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'search_from_table', json=send_data_json)
        r = json.loads(r.text)
        send_data = {
            "table": "companys",
            'user_id': r['description'][0]['user_id'],
            'email': r['description'][0]['account']
        }
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'add_to_table', json=send_data_json)
        r = json.loads(r.text)
        print(r)


class companyLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/company_login.ui', self)
        self.back_BTN.clicked.connect(lambda: changePage(0))
        self.email_input.setMaxLength(50)
        self.email_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))
        self.password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        self.password_input.setMaxLength(15)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.go_forget_ps_BTN.clicked.connect(lambda: self.reset_leavePage(3))
        self.login_BTN.clicked.connect(self.checkLogin)
        self.go_join_BTN.clicked.connect(lambda: self.reset_leavePage(1))

    def reset_leavePage(self, page):
        changePage(page)
        self.email_input.clear()
        self.password_input.clear()
        self.info_label.setText('')

    def checkLogin(self):
        print('pwd=', self.password_input.text())
        print("company_checkLogin--------------------")
        send_data = {
            "account": self.email_input.text(),
            "password": self.password_input.text(),
            "iscompany": isCompany}
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'check_password', json=send_data_json)
        r = json.loads(r.text)
        global user_id
        print('company_checkLogin--------------------', r)
        if r["status"] == 'ok':
            user_id = r['description']['user_id']
            addCompanyInterface.loading_data()  # 導入初始對應資料(如果有的話)
            addCompanyInterface.control_input(False)
            self.info_label.setText('')
            changePage(4)
        else:  # 錯誤訊息
            self.info_label.setText('請檢查帳號密碼')


class forgetPSWindow(QMainWindow):  #####other
    def __init__(self):
        super().__init__()
        loadUi('UI/forget_password.ui', self)
        self.back_BTN.clicked.connect(lambda: self.reset_leavePage(0))
        self.email_input.setMaxLength(50)
        self.email_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))
        self.reset_BTN.clicked.connect(self.check_data_exist)

    def reset_leavePage(self, page):
        changePage(page)
        self.email_input.clear()
        self.info_label.setText('')

    def check_data_exist(self):  ##############################確認其資料後，進入更改介面
        # if    ######################################################判斷成功後
        send_data = {
            'account': self.email_input.text()
        }
        send_data = json.dumps(send_data)

        r = requests.post(url + 'send_mail', json=send_data)

        r = json.loads(r.text)
        print(r)
        if r['status'] == 'err':
            self.info_label.setText(r['description'])
        else:
            self.info_label.setText(r['description'])
            self.reset_leavePage(2)
        # reply = QMessageBox.information(self, '信息', '請至註冊信箱查收更改密碼信函', QMessageBox.Ok | QMessageBox.Close)
        # self.reset_leavePage(2)
        # else:
        # self.info_label.setText('資料不相符，請確認後再輸入')


class companyInterfaceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/company_interface.ui', self)
        self.logout_BTN.clicked.connect(lambda: self.leavePage_function(0))
        self.job_manage_BTN.clicked.connect(self.go_job_manage)
        self.update_save_BTN.clicked.connect(self.update_modify)
        self.email_input.setMaxLength(50)
        self.email_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))
        self.employee_input.setMaxLength(50)
        self.employee_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))

        # self.loading_data()         #導入初始對應資料(如果有的話)

    def go_job_manage(self):
        # TODO job_manage
        print('go_job_manage')
        reply = self.leave_page()
        print(reply)

        if reply == 2048:
            self.upload_data()
            changePage(5)
            addJobManagement.search_job_item()
        elif reply == 2097152:
            changePage(0)  ###不用會卡視窗
            changePage(4)
        else:
            changePage(5)
            addJobManagement.search_job_item()
            self.leavePage_function(5)
        pass

    def loading_data(self):
        print(user_id)
        send_data = {
            'table': 'companys',
            'user_id': user_id
        }
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'search_from_table', json=send_data_json)
        r = json.loads(r.text)
        print(r)

        self.company_name_input.setText(r['description'][0]['name'])
        self.address_input.setText(r['description'][0]['address'])
        # TODO department_comboBox change to edit?
        self.department_comboBox.setCurrentText(r['description'][0]['industry'])
        self.profile_input.setText(r['description'][0]['profile'])
        self.email_input.setText(r['description'][0]['email'])
        self.employee_input.setText(r['description'][0]['employees'])

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
            self.upload_data()  # 上傳資料
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

        send_data = {'table': 'companys', 'user_id': user_id, 'name': self.company_name_input.text(),
                     'address': self.address_input.toPlainText(), 'email': self.email_input.text(),
                     'employees': self.employee_input.text(), 'industry': department,
                     'profile': self.profile_input.toPlainText()}
        print(send_data)
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'add_to_table', json=send_data_json)  # 上傳公司介面資料
        r = json.loads(r.text)
        print(r)

    def leave_page(self):
        if self.company_name_input.isEnabled() == True:
            reply = QMessageBox.information(self, '提示', '您的履歷表尚未儲存', QMessageBox.Save | QMessageBox.Close)
            return reply
        else:
            return -1

    def leavePage_function(self, page):

        reply = self.leave_page()
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
        self.job_item_list = []
        self.applicant_list = []
        self.current_job_id = None
        self.telephone_input.setMaxLength(20)
        self.telephone_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))
        self.salary_input.setMaxLength(20)
        self.salary_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))

        self.back_BTN.clicked.connect(lambda: changePage(4))
        self.logout_BTN.clicked.connect(self.reset_all)
        self.update_save_BTN.clicked.connect(self.update_save)
        self.head_hunter_BTN.clicked.connect(lambda: changePage(6))
        self.interviewer_comboBox.currentIndexChanged.connect(self.resume_list)
        self.add_job_and_manage_comboBox.currentIndexChanged.connect(self.job_want_list)
        self.salary_type_comboBox.currentIndexChanged.connect(self.activate_salary_input)
        self.stackedWidget.hide()

        self.interviewer_comboBox.addItem('只是測試')  ##########測試顯示第2頁面

        self.accept_BTN.clicked.connect(self.send_accept_request)
        self.reject_BTN.clicked.connect(self.send_reject_request)

    # def send_accept_request(self):
    ###################################################################傳送同意結果
    # self.decision_BTN_off()

    # def send_reject_request(self):
    ###################################################################傳送拒絕結果
    # self.decision_BTN_off()

    def send_accept_request(self):
        send_data = {'table': 'applys',
                     'user_id': self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['user_id'],
                     'job_id': self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['job_id'],
                     'status': 'Accept'}
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'add_to_table', json=send_data_json)
        r = json.loads(r.text)
        if r['status'] == 'ok':
            self.accept_BTN.setEnabled(False)
            self.reject_BTN.setEnabled(False)
            self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['status'] = 'Accept'
            # TODO 增加 result info
            # self.result_label.setText('Accept')

    def send_reject_request(self):
        send_data = {'table': 'applys',
                     'user_id': self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['user_id'],
                     'job_id': self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['job_id'],
                     'status': 'Reject'}
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'add_to_table', json=send_data_json)
        r = json.loads(r.text)
        if r['status'] == 'ok':
            self.accept_BTN.setEnabled(False)
            self.reject_BTN.setEnabled(False)
            self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['status'] = 'Reject'
            # self.result_label.setText('Accept')

    def salary_type_change(self):
        if self.salary_type_comboBox.currentIndex() == 1:
            self.salary_input.setText(
                str(self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['hourSalary']))
        elif self.salary_type_comboBox.currentIndex() == 2:
            self.salary_input.setText(
                str(self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['daySalary']))

        elif self.salary_type_comboBox.currentIndex() == 3:
            self.salary_input.setText(
                str(self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['monthSalary']))

        elif self.salary_type_comboBox.currentIndex() == 4:
            self.salary_input.setText(
                str(self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['yearSalary']))

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
            if self.add_job_and_manage_comboBox.currentIndex() != 1:
                self.salary_type_change()
        else:
            self.salary_input.setEnabled(False)
            self.salary_input.setText('')

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
        # TODO resume list
        if self.interviewer_comboBox.currentIndex() == 0 and self.add_job_and_manage_comboBox.currentIndex() > 0:
            self.stackedWidget.setCurrentIndex(0)
        if self.interviewer_comboBox.currentIndex() == 0:
            self.update_save_BTN.setEnabled(True)
        elif self.interviewer_comboBox.currentIndex() > 0:
            self.update_save_BTN.setEnabled(False)
            self.stackedWidget.setCurrentIndex(1)
            if self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['status'] == 'No Reply':
                self.accept_BTN.setEnabled(True)
                self.reject_BTN.setEnabled(True)
            else:
                self.accept_BTN.setEnabled(False)
                self.reject_BTN.setEnabled(False)
            self.name_label.setText(self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['name'])
            self.gender_label.setText(self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['gender'])
            self.age_label.setText(str(self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['age']))
            self.soilder_label.setText(self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['military'])
            self.educarion_label.setText(self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['education'])
            self.school_label.setText(self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['school'])
            self.skill_label.setText(self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['skill'])
            self.profile_label.setText(self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['profile'])
            self.phone_label.setText(self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['phone'])
            self.address_label.setText(self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['address'])
            self.department_label.setText(
                self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['department'])
            self.place_label.setText(self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['place'])
            self.email_label.setText(self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['email'])

            if self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['yearSalary'] == 0:
                self.salary_type.setText('面議')
                self.salary_label.setText('')
            else:
                self.salary_type.setText('月薪')
                self.salary_label.setText(
                    str(self.applicant_list[self.interviewer_comboBox.currentIndex() - 1]['monthSalary']))

    def job_want_list(self):
        self.interviewer_comboBox.setCurrentIndex(0)
        if self.add_job_and_manage_comboBox.currentText() == '新增工作職缺項目':
            self.head_hunter_BTN.setEnabled(False)
            # 新增時清空欄位
            self.current_job_id = None
            self.company_name_show.setText('')
            self.type_comboBox.setCurrentIndex(0)
            self.applicant_show.setText('')
            # TODO 好像沒有地址欄位
            self.address_input.setPlainText('')
            self.place_comboBox.setCurrentText('')
            self.salary_type_comboBox.setCurrentText('面議')
            self.salary_input.setText('')
            self.skill_input_2.setPlainText('')
            self.profile_input_2.setPlainText('')
            self.telephone_input.setText('')
            # TODO 清空

            self.activate_add_new()
            self.post_time_show.setText(QtCore.QDate.currentDate().toString(QtCore.Qt.ISODate))
        elif self.add_job_and_manage_comboBox.currentText() == '-':
            self.head_hunter_BTN.setEnabled(False)
            self.current_job_id = None
            self.stackedWidget.hide()
        elif self.add_job_and_manage_comboBox.currentIndex() > 1:
            self.head_hunter_BTN.setEnabled(True)
            self.current_job_id = self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['job_id']
            print('current_job_id==', self.current_job_id)
            self.activate_add_new()
            self.search_applicant_item(
                self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['job_id'])
            print(self.add_job_and_manage_comboBox.currentIndex(), "count", self.add_job_and_manage_comboBox.count())
            self.company_name_show.setText(
                self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['title'])
            self.type_comboBox.setCurrentText(
                self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['employment_type'])
            self.applicant_show.setText(
                str(self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['applicants']))
            # TODO 好像沒有地址欄位
            self.address_input.setPlainText(
                self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['place'])
            self.place_comboBox.setCurrentText(
                self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['place'])
            if self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['yearSalary'] == 0:
                self.salary_type_comboBox.setCurrentText('面議')
                self.salary_input.setText('')
            else:
                self.salary_type_comboBox.setCurrentText('月薪')
                self.salary_input.setText(
                    str(self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['monthSalary']))
            self.skill_input_2.setPlainText(
                self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['qualifications_skills'])
            self.profile_input_2.setPlainText(
                self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['description'])
            self.telephone_input.setText(
                self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2]['phone'])

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
                hourSalary = 0
                daySalary = 0
                monthSalary = 0
                yearSalary = 0

            send_data = {'table': 'jobs', 'user_id': user_id,
                         'title': self.company_name_show.text(),
                         'employment_type': self.type_comboBox.currentText(), 'phone': self.telephone_input.text(),
                         'place': self.place_comboBox.currentText(),
                         'qualifications_skills': self.skill_input_2.toPlainText(),
                         'description': self.profile_input_2.toPlainText(),
                         'applicants': 0,
                         'hourSalary': hourSalary, 'daySalary': daySalary,
                         'monthSalary': monthSalary, 'yearSalary': yearSalary,
                         # 'post_time': self.post_time_show.text(), 'address': self.address_input.toPlainText()
                         }
            if self.add_job_and_manage_comboBox.currentIndex() > 1:
                send_data = {**send_data,
                             'job_id': self.job_item_list[self.add_job_and_manage_comboBox.currentIndex() - 2][
                                 'job_id']}
            print('send_data---', send_data)
            send_data_json = json.dumps(send_data)
            r = requests.post(url + 'add_to_table', json=send_data_json)  # 上傳公司介面資料
            r = json.loads(r.text)
            print(r)
            #######################################################################################傳送儲存新資料

            if self.add_job_and_manage_comboBox.currentIndex() == 1:  # 新增時

                self.add_job_and_manage_comboBox.addItem(
                    '{}, {}'.format(send_data['title'], send_data['employment_type']))  # 添加進列表中
                # 更新job_item_list
                search_rsp = requests.post(url + 'search_from_table', json=send_data_json)
                search_rsp = json.loads(search_rsp.text)
                print('search_rsp=========', search_rsp)
                if search_rsp['status'] == 'OK':
                    for item in search_rsp['description']:
                        print(item)
                        self.job_item_list.append(item)
                # 清空欄位
                self.company_name_show.setText('')
                self.type_comboBox.setCurrentIndex(0)
                self.applicant_show.setText('')
                # TODO 好像沒有地址欄位
                self.address_input.setPlainText('')
                self.place_comboBox.setCurrentText('')
                self.salary_type_comboBox.setCurrentText('面議')
                self.salary_input.setText('')
                self.skill_input_2.setPlainText('')
                self.profile_input_2.setPlainText('')
                self.telephone_input.setText('')

    def reset_all(self):
        self.company_name_show.clear()
        self.type_comboBox.setCurrentIndex(0)
        self.post_time_show.clear()
        self.applicant_show.setText('0')
        self.telephone_input.clear()
        self.address_input.clear()
        # self.work_where_comboBox.setCurrentIndex(0)
        self.salary_type_comboBox.setCurrentIndex(0)
        # self.want_salary_input.clear()
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

    def search_applicant_item(self, job_id):
        # TODO search_applicant_itme
        self.applicant_list = []
        print("job_id====", job_id)
        send_data = {
            'job_id': job_id, 'originate': 'user'
        }
        send_data_json = json.dumps(send_data)
        applicant_rsp = requests.post(url + 'applicant_search', json=send_data_json)
        applicant_rsp = json.loads(applicant_rsp.text)
        self.interviewer_comboBox.clear()
        self.interviewer_comboBox.addItem('{}'.format('-'))
        print("search_applicant_item", applicant_rsp)
        if applicant_rsp['status'] == 'OK':
            for applicant in applicant_rsp['description']:
                self.applicant_list.append(applicant)
                self.interviewer_comboBox.addItem('{}, {}'.format(applicant['name'], applicant['department']))

    def search_job_item(self):
        self.job_item_list = []
        # TODO search_job_item
        send_data = {
            'table': 'jobs',
            # TODO user id test
            'user_id': user_id
        }
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'search_from_table', json=send_data_json)
        r = json.loads(r.text)
        self.add_job_and_manage_comboBox.setCurrentIndex(0)
        self.interviewer_comboBox.setCurrentIndex(0)
        self.add_job_and_manage_comboBox.clear()
        self.interviewer_comboBox.clear()
        self.add_job_and_manage_comboBox.addItem('{}'.format('-'))
        self.add_job_and_manage_comboBox.addItem('{}'.format('新增工作職缺項目'))
        self.interviewer_comboBox.addItem('{}'.format('-'))
        # TODO test
        self.interviewer_comboBox.addItem('{}'.format('只是測試'))

        print('search_job_item', r)
        if r['status'] == 'OK':
            for item in r['description']:
                self.job_item_list.append(item)
                self.add_job_and_manage_comboBox.addItem('{}, {}'.format(item['title'], item['employment_type']))


class companySearchEngineWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/company_search_engine.ui', self)
        self.resume_search_response = None
        self.index = None
        self.back_BTN.clicked.connect(lambda: self.reset_leavePage(5))
        self.search_BTN.setStyleSheet("QPushButton{border-image: url(UI/magnifying_glass.png)}")
        self.search_BTN.clicked.connect(self.search_go)
        self.salary_type_comboBox.currentIndexChanged.connect(self.activate_salary_input)

    def activate_salary_input(self):
        if self.salary_type_comboBox.currentIndex() != 0:
            self.salary_input.setEnabled(True)
            if self.add_job_and_manage_comboBox.currentIndex() != 1:
                self.salary_type_change()
        else:
            self.salary_input.setEnabled(False)
            self.salary_input.setText('')

    def reset_leavePage(self, page):
        # self.keyword_input.clear()
        # self.soilder_comboBox.setCurrentIndex(0)
        # self.place_comboBox.setCurrentIndex(0)
        # self.education_comboBox.setCurrentIndex(0)
        # self.salary_type_comboBox.setCurrentIndex(0)
        # self.salary_input.setEnabled(False)
        # self.salary_input.clear()
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

        if self.soilder_comboBox.currentText() == '不提供':
            military = ''
        else:
            military = self.soilder_comboBox.currentText()

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
            hourSalary = None
            daySalary = None
            monthSalary = None
            yearSalary = None

        send_data = {'text': self.keyword_input.text(), 'place': place, 'education': education, 'military': military,
                     'salary': ['hourSalary', hourSalary]}
        if self.place_comboBox.currentIndex() == 0:
            send_data.pop('place')
        if self.education_comboBox.currentIndex() == 0:
            send_data.pop('education')
        if self.soilder_comboBox.currentIndex() == 0:
            send_data.pop('military')
        print(send_data)
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'resume_textSplit_complexSearch', json=send_data_json)
        self.resume_search_response = json.loads(r.text)
        print(self.resume_search_response)
        addSearchPeople.load_data_show()

        ####################################################################上傳搜尋資料

        self.reset_leavePage(7)


class companySearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/company_search_result.ui', self)

        self.logout_BTN.clicked.connect(lambda: self.leave_reset(0))
        self.back_BTN.clicked.connect(lambda: self.leave_reset(6))
        self.listWidget.itemClicked.connect(self.go_see_detail)
        # self.load_data_show()

    #################################################################################需在進此頁面前觸發導入結果資料的function


    def leave_reset(self, page):
        self.listWidget.clear()
        changePage(page)

    def load_data_show(self):
        ################################################################讀取搜尋進listWidget
        # TODO load_data_show
        self.listWidget.clear()
        resume_item = addCompanySearchEngine.resume_search_response
        for resume in resume_item['description']:
            self.listWidget.addItem(
                '{}, {}'.format(resume['name'], resume['department'])
            )

    def go_see_detail(self):
        # print(self.listWidget.currentRow())
        print(self.listWidget.currentRow())
        self.index = self.listWidget.currentRow()
        addLookResume.load_data()
        # send_data = self.example_data({'company_name' : self.example_data[self.listWidget.currentRow()]['company_name'], 'job_title' : self.example_data[self.listWidget.currentRow()]['job_title'], 'post_data' : self.example_data[self.listWidget.currentRow()]['post_date']})

        #####################################################################################################將點選到的資料上傳

        changePage(8)


class lookResumeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/company_look_resume.ui', self)
        self.back_BTN.clicked.connect(lambda: self.leave_reset(7))
        self.send_resume_BTN.clicked.connect(self.send_invite)
        self.select_user_id = None
        # self.loading_data()

    # def send_resume(self):
    ####################################################################送出求職訊息

    def load_data(self):
        ###################################################################接收要顯示的訊息
        response = addCompanySearchEngine.resume_search_response
        response = response['description'][addSearchPeople.index]
        self.select_user_id = response['user_id']
        # example_data = {'name': '王小琪', 'phone': '0978996135', 'gender': '女', 'address': '嘉義縣太保市', 'age': '30',
        #                 'soilder': '不提供', 'email': 'siaoba@gmail.com', 'education': '博士', 'school': '國立中央大學',
        #                 'department': '化工所', 'salary_type': '月薪', 'salary': '50000', 'place': '台南市',
        #                 'skill': '須具備python, java基礎', 'profile': '招9晚6，中間休2小'}

        self.name_show.setText(response['name'])
        self.phone_show.setText(response['phone'])
        self.gender_show.setText(response['gender'])
        self.age_show.setText(str(response['age']))
        self.address_show.setText(response['address'])
        self.soilder_show.setText(response['military'])
        self.email_show.setText(response['email'])
        self.educatioin_show.setText(response['education'])
        self.school_show.setText(response['school'])
        self.department_show.setText(response['department'])
        self.place_show.setText(response['place'])
        self.skill_show.setText(response['skill'])
        self.profile_show.setText(response['profile'])

        if response['yearSalary'] == 0:
            self.salary_type_show.setText('面議')
            self.salary_show.setText('')
        else:
            print(addCompanySearchEngine.salary_type_comboBox.currentText())
            if addCompanySearchEngine.salary_type_comboBox.currentText() == '時薪':
                self.salary_type_show.setText('時薪')
                self.salary_show.setText(str(response['hourSalary']))
            elif addCompanySearchEngine.salary_type_comboBox.currentText() == '日薪':
                self.salary_type_show.setText('日薪')
                self.salary_show.setText(str(response['daySalary']))
            elif addCompanySearchEngine.salary_type_comboBox.currentText() == '月薪':
                self.salary_type_show.setText('月薪')
                self.salary_show.setText(str(response['monthSalary']))
            elif addCompanySearchEngine.salary_type_comboBox.currentText() == '年薪':
                self.salary_type_show.setText('年薪')
                self.salary_show.setText(str(response['yearSalary']))
            else:
                self.salary_type_show.setText('面議')
                self.salary_show.setText('')

    def send_invite(self):
        ###########################################################################送出面試邀約

        #########################################################################避免重複投同項工作?
        send_data = {'table': 'applys', 'user_id': self.select_user_id,
                     'job_id': addJobManagement.current_job_id, 'originate': 'company', 'status': 'No Reply'}
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'add_to_table', json=send_data_json)
        r = json.loads(r.text)
        print(r)
        if r['status']=='ok':
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

    wiget.addWidget(addMainWindow)  # 初始頁 0
    wiget.addWidget(addCompanyRegisterPage)  # 註冊頁 1
    wiget.addWidget(addCompanyLoginPage)  # 登入頁 2
    wiget.addWidget(addforgetPSWindow)  # 忘記密碼 3
    wiget.addWidget(addCompanyInterface)  # 公司主畫面 4
    wiget.addWidget(addJobManagement)  # 管理頁 5
    wiget.addWidget(addCompanySearchEngine)  # 搜尋引擎 6
    wiget.addWidget(addSearchPeople)  # 搜尋結果 7
    wiget.addWidget(addLookResume)  # 看履歷頁 8

    wiget.setMinimumSize(800, 600)
    wiget.show()

    sys.exit(app.exec_())
