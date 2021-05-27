import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QMessageBox

#####################################################收取資料
#####################################################收集資料容器

def lookResumeWindowPage():
    wiget.setCurrentIndex(12)

def companySearchPeoplePage():
    wiget.setCurrentIndex(11)

def lookCompanyPage():
    wiget.setCurrentIndex(10)

def userSearchPage():
    wiget.setCurrentIndex(9)

def changeInterfacePage():
    wiget.setCurrentIndex(8)

def companyResumePage():
    wiget.setCurrentIndex(7)

def userResumePage():
    wiget.setCurrentIndex(6)

def forgetPSPage():
    wiget.setCurrentIndex(5)

def companyLoginPage():
    wiget.setCurrentIndex(4)

def userLoginPage():
    wiget.setCurrentIndex(3)

def companyRegisterPage():
    wiget.setCurrentIndex(2)

def userRegisterPage():
    wiget.setCurrentIndex(1)

def backInit():
    wiget.setCurrentIndex(0)


class initialWindow(QMainWindow):
    def __init__(self):
        super(initialWindow, self).__init__()
        loadUi('initial.ui', self)
        self.company_join_BTN.clicked.connect(companyRegisterPage)
        self.company_login_BTN.clicked.connect(companyLoginPage)


        self.user_join_BTN.clicked.connect(userRegisterPage)
        self.user_login_BTN.clicked.connect(userLoginPage)
    
class companyRegisterWindow(QMainWindow):                                               ##公司相關介面
    def __init__(self):
        super(companyRegisterWindow, self).__init__()
        loadUi('company_register.ui', self)
        self.back_BTN.clicked.connect(backInit)
        self.email_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))
        self.phone_num_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))
        self.phone_num_input.setMaxLength(10)
        self.password_input.setMaxLength(15)
        self.password_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        self.confirm_password_input.setMaxLength(15)
        self.confirm_password_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.confirm_password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        self.send_btn.clicked.connect(self.check_info)
        self.go_login_BTN.clicked.connect(companyLoginPage)

    def check_info(self):
        if self.email_input.text() == '' or self.phone_num_input.text() == '' or self.password_input.text() == '' or self.confirm_password_input.text() == '' or self.company_input.text() == '':
            self.info_label.setText('請檢察是否有空欄位')
        else:
            if len(self.email_input.text()) <= 5:
                self.info_label.setText('Email格式有誤')
            else:
                if len(self.phone_num_input.text()) == 10:
                    if self.email_input.text()[-4:] == '.com' and '@' in self.email_input.text() and self.email_input.text().count('@') ==1 and self.email_input.text()[0] != '@' :

                        if len(self.password_input.text()) >= 6 and len(self.password_input.text()) <=15:
                            if len(self.confirm_password_input.text()) >= 6 and len(self.confirm_password_input.text()) <=15:
                                if self.password_input.text() == self.confirm_password_input.text():
                                    reply = QMessageBox.information(self, '信息', '您的註冊已完成，點擊跳轉至登入頁面', QMessageBox.Ok | QMessageBox.Close)
                                        # print(reply)
                                    if reply == 1024:
                                        companyLoginPage()
                                        self.email_input.clear()
                                        self.phone_num_input.clear()
                                        self.password_input.clear()
                                        self.confirm_password_input.clear()
                                        self.company_input.clear()
                                        self.info_label.setText('')
                                    else:
                                        backInit()
                                else:
                                    self.info_label.setText('兩者密碼不一致')
                            else:
                                self.info_label.setText('確認密碼長度錯誤')
                        else:
                            self.info_label.setText('密碼長度錯誤')
                    else:
                        self.info_label.setText('Email格式錯誤')
                else:
                    self.info_label.setText('手機號碼長度錯誤')

class companyLoginWindow(QMainWindow):
    def __init__(self):
        super(companyLoginWindow, self).__init__()
        loadUi('company_login.ui', self)
        self.back_BTN.clicked.connect(backInit)
        self.email_phone_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))
        self.password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        self.password_input.setMaxLength(15)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.go_forget_ps_BTN.clicked.connect(forgetPSPage)
        self.login_BTN.clicked.connect(self.checkLogin)
        self.go_join_BTN.clicked.connect(companyRegisterPage)

    def checkLogin(self):       ########################################完成取得資料後寫帳密核對
        companyResumePage()

class companyInterfaceWindow(QMainWindow):
    def __init__(self):
        super(companyInterfaceWindow, self).__init__()
        loadUi('company_interface.ui', self)
        self.logout_BTN.clicked.connect(backInit)
        self.job_search.clicked.connect(self.search_people)

    def search_people(self):     ####################################想想收尋方式,顯示方式
        companySearchPeoplePage()


class companySearchWindow(QMainWindow):
    def __init__(self):
        super(companySearchWindow, self).__init__()
        loadUi('company_search_interface.ui', self)
        self.logout_BTN.clicked.connect(backInit)
        self.back_BTN.clicked.connect(lookCompanyPage)
        self.look_resume_BTN.clicked.connect(self.look_resume)

    def look_resume(self):
        lookResumeWindowPage()

class lookResumeWindow(QMainWindow):
    def __init__(self):
        super(lookResumeWindow, self).__init__()
        loadUi('look_user_resume.ui', self)
        self.back_BTN.clicked.connect(companySearchPeoplePage)
        self.logout_BTN.clicked.connect(backInit)

class userRegisterWindow(QMainWindow):                                                  ##一般用戶介面
    def __init__(self):
        super(userRegisterWindow, self).__init__()
        loadUi('user_register.ui', self)
        self.back_BTN.clicked.connect(backInit)
        self.email_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))
        self.phone_num_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))
        self.phone_num_input.setMaxLength(10)
        self.password_input.setMaxLength(15)
        self.password_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        self.confirm_password_input.setMaxLength(15)
        self.confirm_password_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.confirm_password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        self.send_btn.clicked.connect(self.check_psw)
        self.go_login_BTN.clicked.connect(userLoginPage)


    def check_psw(self):
        if self.email_input.text() == '' or self.phone_num_input.text() == '' or self.password_input.text() == '' or self.confirm_password_input.text() == '':
            self.info_label.setText('請檢察是否有空欄位')
        else:
            if len(self.email_input.text()) <= 5:
                self.info_label.setText('Email格式有誤')
            else:
                if len(self.phone_num_input.text()) == 10:
                    if self.email_input.text()[-4:] == '.com' and '@' in self.email_input.text() and self.email_input.text().count('@') ==1 and self.email_input.text()[0] != '@' :

                        if len(self.password_input.text()) >= 6 and len(self.password_input.text()) <=15:
                            if len(self.confirm_password_input.text()) >= 6 and len(self.confirm_password_input.text()) <=15:
                                if self.password_input.text() == self.confirm_password_input.text():
                                    reply = QMessageBox.information(self, '信息', '您的註冊已完成，點擊跳轉至登入頁面', QMessageBox.Ok | QMessageBox.Close)
                                     # print(reply)
                                    if reply == 1024:
                                        userLoginPage()
                                        self.email_input.clear()
                                        self.phone_num_input.clear()
                                        self.password_input.clear()
                                        self.confirm_password_input.clear()
                                        self.info_label.setText('')                       
                                    else:
                                        backInit()
                                else:
                                   self.info_label.setText('兩者密碼不一致')
                            else:
                                self.info_label.setText('確認密碼長度錯誤')
                        else:
                            self.info_label.setText('密碼長度錯誤')
                    else:
                        self.info_label.setText('Email格式錯誤')
                else:
                    self.info_label.setText('手機號碼長度錯誤')
                
class userLoginWindow(QMainWindow):
    def __init__(self):
        super(userLoginWindow, self).__init__()
        loadUi('user_login.ui', self)
        self.back_BTN.clicked.connect(backInit)
        self.email_phone_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))
        self.password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        self.password_input.setMaxLength(15)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.go_forget_ps_BTN.clicked.connect(forgetPSPage)
        self.login_BTN.clicked.connect(self.checkLogin)
        self.go_join_BTN.clicked.connect(userRegisterPage)

    def checkLogin(self):       ########################################完成取得資料後寫帳密核對
        userResumePage()
        
class userResumeWindow(QMainWindow):
    def __init__(self):
        super(userResumeWindow, self).__init__()
        loadUi('user_resume.ui', self)
        self.logout_BTN.clicked.connect(backInit)
        self.job_search_BTN.clicked.connect(self.search)

    def search(self):       ##########################################收尋條件，maybe再拉一個介面
        userSearchPage()


class userSearchWindow(QMainWindow):    ###################收尋的顯示方式可能還要再研究QQ，要再找一下複製一個個小layout方法，分別想式不同的公司訊息資訊
    def __init__(self):
        super(userSearchWindow, self).__init__()
        loadUi('user_search_interface.ui', self)
        self.logout_BTN.clicked.connect(backInit)
        self.back_BTN.clicked.connect(userResumePage)
        self.look_company_BTN.clicked.connect(self.look_info)

    def look_info(self):            #####################查看對應結果的公司信息
        lookCompanyPage()

class lookCompanyWindow(QMainWindow):    ###################收尋的顯示方式還要再研究QQ
    def __init__(self):
        super(lookCompanyWindow, self).__init__()
        loadUi('look_company_interface.ui', self)
        self.logout_BTN.clicked.connect(backInit)
        self.goBack_BTN.clicked.connect(userSearchPage)

class forgetPSWindow(QMainWindow):    #####other
    def __init__(self):
        super(forgetPSWindow, self).__init__()
        loadUi('forgetPW.ui', self)
        self.back_BTN.clicked.connect(backInit)
        self.email_phone_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9@.]+$")))
        self.reset_BTN.clicked.connect(self.check_data_exist)

    def check_data_exist(self):         ##############################確認其資料後，進入更改介面判斷式
        changeInterfacePage()

class changePSWindow(QMainWindow):
    def __init__(self):
        super(changePSWindow, self).__init__()
        loadUi('change_interface.ui', self)
        self.password_input.setMaxLength(15)
        self.password_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        self.confirm_password_input.setMaxLength(15)
        self.confirm_password_input.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.confirm_password_input.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[A-Za-z0-9]+$")))
        self.finish_BTN.clicked.connect(self.send_reset_data)

    def send_reset_data(self):
        if len(self.password_input.text()) >=6 and len(self.password_input.text()) <= 15:
            if self.password_input.text() == self.confirm_password_input.text():
                reply = QMessageBox.information(self, '信息', '您的密碼重設完成，請重新登入', QMessageBox.Ok)
                # print(reply)
                
                self.password_input.clear()
                self.confirm_password_input.clear()
                self.info_label.setText('')
                backInit()

            else:
                self.info_label.setText('兩組密碼不一致')
        else:
            self.info_label.setText('請確定密碼長度正確')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    wiget = QtWidgets.QStackedWidget()
    addMainWindow = initialWindow()
    addUserRegisterPage = userRegisterWindow()
    addCompanyRegisterPage = companyRegisterWindow()
    addUserLoginPage = userLoginWindow()
    addCompanyLoginPage = companyLoginWindow()
    addForgetPassPage = forgetPSWindow()
    addUserResumePage = userResumeWindow()
    addCompanyInterface = companyInterfaceWindow()
    addChangeInterface = changePSWindow()
    addUserSearch = userSearchWindow()
    addLookCompanyInfo = lookCompanyWindow()
    addSearchPeople = companySearchWindow()
    addLookResume = lookResumeWindow()
	
    wiget.addWidget(addMainWindow)

    wiget.addWidget(addUserRegisterPage)
    wiget.addWidget(addCompanyRegisterPage)
    
    wiget.addWidget(addUserLoginPage)
    wiget.addWidget(addCompanyLoginPage)
    wiget.addWidget(addForgetPassPage)
    wiget.addWidget(addUserResumePage)
    wiget.addWidget(addCompanyInterface)
    wiget.addWidget(addChangeInterface)
    wiget.addWidget(addUserSearch)
    wiget.addWidget(addLookCompanyInfo)
    wiget.addWidget(addSearchPeople)
    wiget.addWidget(addLookResume)

    wiget.setFixedHeight(600)
    wiget.setFixedWidth(800)
    wiget.show()

    sys.exit(app.exec_())