import requests
import json
from flask import Flask, request, jsonify

url = 'http://127.0.0.1:5000/'

# col = {'user_id': 2}
# data3 = json.dumps(col)
# # r = requests.get(url + 'test')
# r = requests.post(url + 'test', json=data3)
# print("{} {} {}".format(r, type(r.text), r.text))
# r = json.loads(r.text)
# print(r['description'])

# send_data = {
#     "account":"kevin@gmail.com",
#     "password":"123456",
#     "iscompany":False}
# send_data_json = json.dumps(send_data)
# r = requests.post(url + 'register_user_account', json=send_data_json)
# =========================
# send_data = {
#     # "job_id": 4,
#     "user_id": 3,
#     "title": "ME engineer",
#     "employment_type": "full-time",
#     "applicants": 16,
#     "description": "這份工作，需要做",
#     "qualifications_skills": "Matlab 精通",
#     "monthSalary": 38000,
#     "place": "台北市",
#     "phone": "0912345678"
# }
# =========================
# contain_search===========================
# send_data = {'title': 'EE ', 'applicants': 25, 'mode': 'or'}
# send_data_json = json.dumps(send_data)
# r = requests.post(url + 'register_jobs', json=send_data_json)
# r = requests.post(url + 'contain_search', json=send_data_json)
# contain_search===========================
# send_data = {'applicants': 25}
# send_data_json = json.dumps(send_data)
# r = requests.post(url + 'job_search', json=send_data_json)
# test===========================
send_data = {'text': 'python full'}
send_data_json = json.dumps(send_data)
r = requests.post(url + 'test', json=send_data_json)

# r = json.loads(r.text)
# print(r['description'])

# print("{} {} {}".format(r, type(r.text), r.text))
# r = json.loads(r.text)
# print(r['description'])

#  UI Test======================================
# class Main:
#     def __init__(self, wiget):
#         self.wiget = wiget
#         self.window(self.change_page(self.wiget))
#
#     class change_page:
#         def __init__(self, wiget):
#             self.wiget = wiget
#             print('a')
#
#         def backInit(self):
#             wiget.setCurrentIndex(0)
#             print('b')
#
#     class initialWindow(QMainWindow):
#         def __init__(self, change_page):
#             self.change_page = change_page
#             self.company_join_BTN.clicked.connect(self.change_page.backInit)
# math = Main("Mathematics")
#  UI Test======================================
