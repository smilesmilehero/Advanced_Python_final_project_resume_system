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
isCompany = False


class presonalInitialWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/personal_init.ui', self)
        self.user_join_BTN.clicked.connect(lambda: changePage(1))
        self.user_login_BTN.clicked.connect(lambda: changePage(2))


class userRegisterWindow(QMainWindow):  ##一般用戶介面
    def __init__(self):
        super().__init__()
        loadUi('UI/user_register.ui', self)
        self.back_BTN.clicked.connect(lambda: self.clear_and_changePage(0))
        self.email_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))

        self.password_input.setMaxLength(15)
        self.password_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))

        self.confirm_password_input.setMaxLength(15)
        self.confirm_password_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.confirm_password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))

        self.send_btn.clicked.connect(self.check_psw)
        self.go_login_BTN.clicked.connect(lambda: self.clear_and_changePage(2))

    def clear_and_changePage(self, page):
        self.email_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.info_label.setText('')
        changePage(page)

    def check_psw(self):
        if self.email_input.text() == '' or self.password_input.text() == '' or self.confirm_password_input.text() == '':
            self.info_label.setText('請檢察是否有空欄位')
        else:
            if len(self.email_input.text()) <= 5:
                self.info_label.setText('Email格式有誤')
            else:
                if (self.email_input.text()[
                   -3:] == '.tw' or self.email_input.text()[
                   -4:] == '.com') and '@' in self.email_input.text() and self.email_input.text().count('@') == 1 and \
                        self.email_input.text()[0] != '@':
                    if len(self.password_input.text()) >= 6 and len(self.password_input.text()) <= 15:
                        if len(self.confirm_password_input.text()) >= 6 and len(
                                self.confirm_password_input.text()) <= 15:
                            if self.password_input.text() == self.confirm_password_input.text():
                                rsp = self.register_company_account()  ############call上傳

                                if rsp == 'err':

                                    self.info_label.setText('帳號已被使用')
                                else:
                                    self.create_resume()
                                    reply = QMessageBox.information(self, '信息', '您的註冊已完成，點擊跳轉至登入頁面',
                                                                    QMessageBox.Ok | QMessageBox.Close)

                                    # print(reply)
                                    if reply == 1024:
                                        changePage(2)
                                        self.email_input.clear()
                                        self.password_input.clear()
                                        self.confirm_password_input.clear()
                                        # self.school_input.clear()
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

    def register_company_account(self):
        print("register_user_account--------------------")
        # iscompany = False
        send_data = {
            "table": "users",
            "account": self.email_input.text(),
            "password": self.password_input.text(),
            # "school": self.school_input.text(),                             #####多學校上傳
            "iscompany": isCompany}
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'add_to_table', json=send_data_json)
        r = json.loads(r.text)
        return r['status']

    def create_resume(self):
        send_data = {
            "table": "users",
            "account": self.email_input.text()
        }
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'search_from_table', json=send_data_json)
        r = json.loads(r.text)
        # print(r)
        send_data = {
            "table": "resumes",
            'user_id': r['description'][0]['user_id'],
            'email': r['description'][0]['account']
        }
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'add_to_table', json=send_data_json)
        r = json.loads(r.text)
        print(r)


class userLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/user_login.ui', self)
        self.back_BTN.clicked.connect(lambda: changePage(0))
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

    def checkLogin(self):  ########################################完成取得資料後寫帳密核對
        # if  ########################################帳密相符
        # self.reset_leavePage(4)

        # # print("check login--------------------")
        # # send_data = {"account":self.email_phone_input.text()}
        # # send_data_json = json.dumps(send_data)

        # # print(send_data_json)
        # # print(type(send_data_json))
        # # r = requests.post(url + 'test', json=send_data_json)
        # # print(r)
        # # print(r.text)
        print('pwd=', self.password_input.text())
        # iscompany = False
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
            addUserResumePage.loading_data()  # 導入初始對應資料(如果有的話)
            self.info_label.setText('')
            self.reset_leavePage(4)
        else:  ########################################錯誤訊息
            # TODO
            # pass
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

    def check_data_exist(self):  ##############################確認其資料後，進入更改介面判斷式
        # changePage(5)
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
            reply = QMessageBox.information(self, '信息', '已寄送您的密碼至信箱，請查收後登入', QMessageBox.Ok)
            self.reset_leavePage(2)
        # changePage(2) ########回到登入頁面

class userResumeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/user_resume.ui', self)

        self.phone_input.setMaxLength(10)
        self.phone_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))

        self.age_input.setMaxLength(3)
        self.age_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))

        self.email_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))

        self.salary_input.setMaxLength(12)
        self.salary_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))

        # self.loading_data()         #導入初始對應資料(如果有的話)

        self.logout_BTN.clicked.connect(lambda: self.leavePage_function(0))
        self.work_search_BTN.clicked.connect(lambda: self.leavePage_function(5))
        self.update_modify_BTN.clicked.connect(self.update_modify)
        self.salary_type_comboBox.currentIndexChanged.connect(self.activate_salary_input)
        self.mail_BTN.clicked.connect(self.go_mail)
        # TODO fun include leavePage addUserMailPage.search

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
        self.department_input.setText('')
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
            hourSalary = 0
            daySalary = 0
            monthSalary = 0
            yearSalary = 0

        if self.gender_comboBox.currentText() == '-':
            gender = ''
        else:
            gender = self.gender_comboBox.currentText()

        if self.education_comboBox.currentText() == '請選擇':
            education = ''
        else:
            education = self.education_comboBox.currentText()

        if self.place_comboBox.currentText() == '請選擇上班地點':
            place = ''
        else:
            place = self.place_comboBox.currentText()

        send_data = {'table': 'resumes', 'user_id': user_id, 'name': self.name_input.text(),
                     'phone': self.phone_input.text(), 'gender': gender, 'age': self.age_input.text(),
                     'address': self.address_input.toPlainText(), 'military': self.soilder_comboBox.currentText(),
                     'education': education, 'email': self.email_input.text(), 'school': self.school_input.text(),
                     'department': self.department_input.text(), 'place': place, 'hourSalary': hourSalary,
                     'daySalary': daySalary,
                     'monthSalary': monthSalary, 'yearSalary': yearSalary, 'skill': self.skill_input.toPlainText(),
                     'profile': self.profile_input.toPlainText()}
        print(send_data)

        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'add_to_table', json=send_data_json)
        r = json.loads(r.text)
        print(r)

    def leave_page(self):
        if self.name_input.isEnabled() == True:
            reply = QMessageBox.information(self, '提示', '您的履歷表尚未儲存',
                                            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Close)
            return reply
        else:
            return -1

    def leavePage_function(self, page):
        reply = self.leave_page()
        # print(reply)
        if reply == 2048:

            self.upload_data()

            # self.reset()
            changePage(page)
        elif reply == 8388608:
            # self.reset()
            changePage(page)
        elif reply == -1:
            # self.reset()
            changePage(page)
        else:
            changePage(0)  ###不用會卡視窗
            changePage(4)

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
        self.department_input.setEnabled(switch)
        self.place_comboBox.setEnabled(switch)
        self.salary_type_comboBox.setEnabled(switch)
        self.skill_input.setEnabled(switch)
        self.profile_input.setEnabled(switch)

    def loading_data(self):  ##############################剛進入履歷畫面的資料導入，若有資訊的話
        # self.control_input(False)
        # global user_id
        print(user_id)
        send_data = {
            'table': 'resumes',
            # 'name':'王小明'
            'user_id': user_id
        }
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'search_from_table', json=send_data_json)
        r = json.loads(r.text)
        print(r)
        self.name_input.setText(r['description'][0]['name'])
        self.phone_input.setText(r['description'][0]['phone'])
        self.gender_comboBox.setCurrentText(r['description'][0]['gender'])
        self.age_input.setText(str(r['description'][0]['age'] if r['description'][0]['age'] != None else ''))
        self.address_input.setText(r['description'][0]['address'])
        self.soilder_comboBox.setCurrentText(r['description'][0]['military'])
        self.education_comboBox.setCurrentText(r['description'][0]['education'])
        self.email_input.setText(r['description'][0]['email'])
        self.school_input.setText(r['description'][0]['school'])
        self.department_input.setText(r['description'][0]['department'])
        self.place_comboBox.setCurrentText(r['description'][0]['place'])
        if r['description'][0]['yearSalary'] == 0:
            self.salary_type_comboBox.setCurrentText('面議')
            self.salary_input.setText('')

        else:
            self.salary_type_comboBox.setCurrentText('月薪')
            self.salary_input.setText(str(r['description'][0]['monthSalary'] if r['description'][0]['monthSalary']!=None else ""))
        self.skill_input.setText(r['description'][0]['skill'])
        self.profile_input.setText(r['description'][0]['profile'])

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


    def go_mail(self):
        reply = self.leave_page()
        if reply == 2048:
            self.upload_data()
            # self.reset()
            changePage(7)
            # print(reply)
            addUserMailPage.search_apply()
        elif reply == 8388608:
            changePage(0)  ###不用會卡視窗
            changePage(4)
            # print(reply)
        else:
            # print(reply)
            # self.reset()
            changePage(7)
            addUserMailPage.search_apply()


class userSearchEngineWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/user_search_engine.ui', self)
        self.back_BTN.clicked.connect(lambda: self.reset_leavePage(4))
        self.search_BTN.setStyleSheet("QPushButton{border-image: url(UI/magnifying_glass.png)}")

        self.salary_input.setMaxLength(12)
        self.salary_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))
        self.search_BTN.clicked.connect(self.send_search)
        self.salary_type_comboBox.currentIndexChanged.connect(self.activate_salary_input)
        self.response = None

    def activate_salary_input(self):
        if self.salary_type_comboBox.currentIndex() != 0:
            self.salary_input.setEnabled(True)
        else:
            self.salary_input.setEnabled(False)

    def reset_leavePage(self, page):
        self.keyword_input.clear()
        self.place_comboBox.setCurrentIndex(0)
        self.salary_type_comboBox.setCurrentIndex(0)
        self.salary_input.setEnabled(False)
        self.salary_input.clear()
        changePage(page)

    def send_search(self):

        if self.place_comboBox.currentText() == '請選擇上班地點':
            place = ''
        else:
            place = self.place_comboBox.currentText()

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

        send_data = {'text': self.keyword_input.text(), 'place': place, 'salary': ['hourSalary', hourSalary]}
        if self.place_comboBox.currentIndex() == 0:
            send_data.pop('place')
        print(send_data)
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'job_textSplit_complexSearch', json=send_data_json)
        self.response = json.loads(r.text)
        print(self.response)
        addUserSearchResult.load_data_show()
        ####################################################################上傳搜尋資料

        self.reset_leavePage(6)
        # changePage(7)
        # self.reset()


class userSearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/user_search_interface.ui', self)
        self.example_data = []
        self.logout_BTN.clicked.connect(lambda: self.leave_reset(0))
        self.back_BTN.clicked.connect(lambda: self.leave_reset(5))
        self.listWidget.itemClicked.connect(self.go_see_detail)
        self.index = None

        # self.load_data_show()

    def leave_reset(self, page):
        self.listWidget.clear()
        changePage(page)

    def load_data_show(self):
        ################################################################讀取搜尋進listWidget

        self.listWidget.clear()
        response = addUserSearchEngine.response

        for job in response['description']:
            self.listWidget.addItem(
                '{}, {}'.format(job['name'], job['title'])
            )

    def go_see_detail(self):
        # TODO 將點選到的資料上傳
        print(self.listWidget.currentRow())
        self.index = self.listWidget.currentRow()

        # send_data = self.example_data({'company_name' : self.example_data[self.listWidget.currentRow()]['company_name'], 'job_title' : self.example_data[self.listWidget.currentRow()]['job_title'], 'post_data' : self.example_data[self.listWidget.currentRow()]['post_date']})
        ######################################################################################################將點選到的資料上傳
        addLookCompanyInfo.load_data()
        changePage(8)


class userMailWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/user_mail.ui', self)
        self.originate_c = []
        self.originate_u = []
        self.logout_BTN.clicked.connect(lambda: changePage(0))
        self.back_BTN.clicked.connect(lambda: changePage(4))
        # self.back_BTN.clicked.connect(self.search_apply)

        self.scrollAreaWidgetContents.hide()
        # self.get_user_send_result()
        # self.get_invite()
        self.send_result_comboBox.currentIndexChanged.connect(self.show_result_detail)
        self.invite_comboBox.currentIndexChanged.connect(self.show_invite_detail)
        self.accept_BTN.clicked.connect(self.send_accept_request)
        self.reject_BTN.clicked.connect(self.send_reject_request)

    def send_accept_request(self):  ##################################################################傳送同意結果
        send_data = {'table': 'applys', 'user_id': user_id,
                     'job_id': self.originate_c[self.invite_comboBox.currentIndex() - 1]['job_id'], 'status': 'Accept'}
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'add_to_table', json=send_data_json)
        r = json.loads(r.text)
        if r['status'] == 'ok':
            self.accept_BTN.setEnabled(False)
            self.reject_BTN.setEnabled(False)
            self.result_label.setText('Accept')

    def send_reject_request(self):  ##################################################################傳送拒絕結果
        send_data = {'table': 'applys', 'user_id': user_id,
                     'job_id': self.originate_c[self.invite_comboBox.currentIndex() - 1]['job_id'], 'status': 'Reject'}
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'add_to_table', json=send_data_json)
        r = json.loads(r.text)
        if r['status'] == 'ok':
            self.accept_BTN.setEnabled(False)
            self.reject_BTN.setEnabled(False)
            self.result_label.setText('Reject')

    def decision_BTN_off(self):
        send_data = {'table': 'applys', 'user_id': user_id,
                     'job_id': self.originate_c[self.invite_comboBox.currentIndex() - 1]['job_id']}
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'search_from_table', json=send_data_json)
        r = json.loads(r.text)
        if r['status'] == 'OK':
            ans_status = r['description'][0]['status']
            print('ans_status', ans_status)
            self.result_label.setText(ans_status)
            if ans_status == 'No Reply':
                self.accept_BTN.setEnabled(True)
                self.reject_BTN.setEnabled(True)
            else:
                self.accept_BTN.setEnabled(False)
                self.reject_BTN.setEnabled(False)
        else:
            print('apply search sql fail')

    def show_result_detail(self):
        if self.send_result_comboBox.currentText() == '-':
            self.scrollAreaWidgetContents.hide()
            self.result_label.setText('')

        elif self.send_result_comboBox.currentIndex() > 0:
            print(self.send_result_comboBox.currentIndex())
            self.invite_comboBox.setCurrentIndex(0)
            self.company_name_show.setText(self.originate_u[self.send_result_comboBox.currentIndex() - 1]['title'])
            self.type_comboBox.setText(
                self.originate_u[self.send_result_comboBox.currentIndex() - 1]['employment_type'])
            self.applicant_show.setText(
                str(self.originate_u[self.send_result_comboBox.currentIndex() - 1]['applicants']))
            self.work_where_comboBox.setCurrentText(
                self.originate_u[self.send_result_comboBox.currentIndex() - 1]['place'])
            self.address_input.setPlainText(self.originate_u[self.send_result_comboBox.currentIndex() - 1]['address'])
            self.skill_input.setPlainText(
                self.originate_u[self.send_result_comboBox.currentIndex() - 1]['qualifications_skills'])
            self.profile_input.setPlainText(
                self.originate_u[self.send_result_comboBox.currentIndex() - 1]['description'])

            self.post_dateEdit.setText(
                self.originate_u[self.send_result_comboBox.currentIndex() - 1]['post_time'][:-12])
            self.telephone_input.setText(self.originate_u[self.send_result_comboBox.currentIndex() - 1]['phone'])
            if self.originate_u[self.send_result_comboBox.currentIndex() - 1]['yearSalary'] == 0:
                self.salary_type_comboBox.setCurrentText('面議')
                self.want_salary_input.setText('')
            else:
                self.salary_type_comboBox.setCurrentText('月薪')
                self.want_salary_input.setText(
                    str(self.originate_u[self.send_result_comboBox.currentIndex() - 1]['monthSalary']))

            self.result_label.setText(self.originate_u[self.send_result_comboBox.currentIndex() - 1]['status'])
            self.scrollAreaWidgetContents.show()

            self.accept_BTN.hide()
            self.reject_BTN.hide()

    def show_invite_detail(self):
        if self.invite_comboBox.currentText() == '-':
            self.scrollAreaWidgetContents.hide()
            self.result_label.setText('')
        elif self.invite_comboBox.currentIndex() > 0:
            self.send_result_comboBox.setCurrentIndex(0)

            self.company_name_show.setText(self.originate_c[self.invite_comboBox.currentIndex() - 1]['title'])
            self.type_comboBox.setText(
                self.originate_c[self.invite_comboBox.currentIndex() - 1]['employment_type'])
            self.applicant_show.setText(
                str(self.originate_c[self.invite_comboBox.currentIndex() - 1]['applicants']))
            self.work_where_comboBox.setCurrentText(
                self.originate_c[self.invite_comboBox.currentIndex() - 1]['place'])
            self.address_input.setPlainText(self.originate_c[self.invite_comboBox.currentIndex() - 1]['address'])
            self.skill_input.setPlainText(
                self.originate_c[self.invite_comboBox.currentIndex() - 1]['qualifications_skills'])
            self.profile_input.setPlainText(
                self.originate_c[self.invite_comboBox.currentIndex() - 1]['description'])

            self.post_dateEdit.setText(
                self.originate_c[self.invite_comboBox.currentIndex() - 1]['post_time'][:-12])
            self.telephone_input.setText(self.originate_c[self.invite_comboBox.currentIndex() - 1]['phone'])
            if self.originate_c[self.invite_comboBox.currentIndex() - 1]['yearSalary'] == 0:
                self.salary_type_comboBox.setCurrentText('面議')
                self.want_salary_input.setText('')
            else:
                self.salary_type_comboBox.setCurrentText('月薪')
                self.want_salary_input.setText(
                    str(self.originate_c[self.invite_comboBox.currentIndex() - 1]['monthSalary']))

            self.result_label.setText(self.originate_c[self.send_result_comboBox.currentIndex() - 1]['status'])
            self.scrollAreaWidgetContents.show()
            self.accept_BTN.show()
            self.reject_BTN.show()
            self.decision_BTN_off()

    def search_apply(self):
        send_data = {
            'user_id': user_id
        }
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'apply_search', json=send_data_json)
        r = json.loads(r.text)
        print('apply=', r)
        self.invite_comboBox.setCurrentIndex(0)
        self.send_result_comboBox.setCurrentIndex(0)
        self.invite_comboBox.clear()
        self.send_result_comboBox.clear()
        self.invite_comboBox.addItem('{}'.format('-'))
        self.send_result_comboBox.addItem('{}'.format('-'))
        self.originate_c=[]
        self.originate_u=[]

        if r['status'] == 'OK':
            for item in r['description']:
                if item['originate'] == 'company':
                    self.originate_c.append(item)
                    self.invite_comboBox.addItem('{}, {}'.format(item['name'], item['title']))
                    # self.address_input.setPlainText(item['address'])
                else:
                    self.originate_u.append(item)
                    self.send_result_comboBox.addItem('{}, {}'.format(item['name'], item['title']))

        # print('from u=',self.originate_u)
        # print('from c=',self.originate_c)

    def get_user_send_result(self):
        #######################################################################################此處取得投遞資料
        print('get_user_send_result=', self.originate_c)
        for item in self.originate_u:
            self.send_result_comboBox.addItem('{}, {}'.format(item['name'], item['title']))

    def get_invite(self):
        #######################################################################################此處取得邀請資料
        # self.invite_comboBox.addItem('慧邦科技，軟體工程師')
        print('get_user_send_result=', self.originate_c)
        for item in self.originate_c:
            self.invite_comboBox.addItem('{}, {}'.format(item['name'], item['title']))

    # def user_send_result(self):


class lookCompanyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('UI/user_look_requirement.ui', self)
        self.back_BTN.clicked.connect(lambda: self.leave_reset(6))
        self.send_resume_BTN.clicked.connect(self.send_invite)
        # self.load_data()
        self.job_id = None
        self.applicants = 0

    # def send_resume(self):
    ####################################################################送出求職訊息

    def load_data(self):
        ###################################################################接收要顯示的訊息
        # example_data = {'job_name': '軟體工程師', 'post_date': '2021/01/30', 'job_type': '工讀', 'phone': '0223917925',
        #                 'applicant': '6', 'address': '台北市中正區', 'place': '台北市', 'salary': '40000',
        #                 'skill': 'python, java', 'profile': '你知道的'}
        response = addUserSearchEngine.response
        response = response['description'][addUserSearchResult.index]
        self.job_id = response['job_id']
        self.applicants = response['applicants']

        self.company_name_show.setText(response['name'])
        self.type_comboBox.setText(response['employment_type'])
        self.dateEdit_2.setText(response['post_time'][:-12])
        self.telephone_input.setText(response['phone'])
        self.applicant_show.setText(str(response['applicants']))
        self.address_input.setPlainText(response['address'])
        self.place_comboBox.setCurrentIndex(self.place_comboBox.findText(response['place']))
        if response['yearSalary'] == 0:
            self.salary_type_comboBox.setCurrentText('面議')
            self.salary_input.setText('')
        else:
            self.salary_type_comboBox.setCurrentText('月薪')
            self.salary_input.setText(str(response['monthSalary']))

        self.skill_require_input.setPlainText(response['qualifications_skills'])
        self.profile_input.setPlainText(response['description'])

    def send_invite(self):
        job_id = self.job_id
        send_data = {'table': 'applys', 'user_id': user_id,
                     'job_id': job_id, 'originate': 'user', 'status': 'No Reply'}
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'add_to_table', json=send_data_json)
        r = json.loads(r.text)
        print(r)

        send_data = {'table': 'jobs', 'job_id': self.job_id, 'applicants': self.applicants + 1}
        send_data_json = json.dumps(send_data)
        r = requests.post(url + 'add_to_table', json=send_data_json)
        r = json.loads(r.text)
        print(r)

        ###########################################################################送出面試邀約
        #########################################################################避免重複投同項工作?

        reply = QMessageBox.information(self, '提示', '成功發送邀約，請耐心等待對方回應', QMessageBox.Ok | QMessageBox.Close)

    def leave_reset(self, page):
        # self.dateEdit_2.disconnect()
        self.company_name_show.clear()
        self.type_comboBox.setText('')
        self.dateEdit_2.setText('')
        self.telephone_input.clear()
        self.applicant_show.setText('')
        self.address_input.clear()
        self.place_comboBox.setCurrentIndex(0)
        self.salary_type_comboBox.setCurrentIndex(0)
        self.skill_require_input.clear()
        self.profile_input.clear()

        changePage(page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wiget = QtWidgets.QStackedWidget()
    addMainWindow = presonalInitialWindow()
    addUserLoginPage = userLoginWindow()
    addUserRegisterPage = userRegisterWindow()
    addForgetPassPage = forgetPSWindow()
    addUserResumePage = userResumeWindow()
    # addChangeInterface = changePSWindow()
    addUserSearchEngine = userSearchEngineWindow()
    addUserSearchResult = userSearchWindow()
    addUserMailPage = userMailWindow()
    addLookCompanyInfo = lookCompanyWindow()

    wiget.addWidget(addMainWindow)  ###初始頁 0

    wiget.addWidget(addUserRegisterPage)  ###註冊頁 1
    wiget.addWidget(addUserLoginPage)  ###登入頁 2
    wiget.addWidget(addForgetPassPage)  ###忘記密碼 3
    wiget.addWidget(addUserResumePage)  ###履歷表頁 4
    wiget.addWidget(addUserSearchEngine)  ###搜尋頁  5
    wiget.addWidget(addUserSearchResult)  ###結果頁  6
    wiget.addWidget(addUserMailPage)  ###小郵箱  7
    wiget.addWidget(addLookCompanyInfo)  ###看工作資訊  8

    wiget.setMinimumSize(800, 600)

    wiget.show()

    sys.exit(app.exec_())
