import requests
import json
from flask import Flask, request, jsonify

url = 'http://127.0.0.1:5000/'

# =========================
# users
# send_data = {
#     "table": "users",
#     "user_id": 4,
#     "account": "ntut@gmail",
#     "password": "12345678",
#     "iscompany": True
# }
# =========================
# =========================
# resumes
# send_data = {
#     "table": "resumes",
#     "user_id": 2,
#     "name": "林小美",
#     "address": "台北市萬華區",
#     "phone": "0912345678",
#     "email": "t109368019@ntut.org.tw",
#     "education": "博士",
#     "school": "臺灣大學",
#     "department": "電子工程系",
#     "skill": "python-精通, 英文-精通",
#     "profile": "大家好，～～",
#     "gender": "女",
#     "age": 23,
#     "military": "免役",
#     "hourSalary": 190,
#     "daySalary": 190*8,
#     "monthSalary": 190*8*30,
#     "yearSalary": 190*8*30*12,
#     "place": "台北市"
# }
# =========================
# =========================
# companys
# send_data = {
#     "table": "companys",
#     "user_id": 4,
#     "name": "NTUT",
#     "address": "台北市大安區",
#     "employees": "1000+",
#     "industry": "電子產業",
#     "description": "本校成立於......",
#     "mail": "t109368019@ntut.org.tw"
# }
# =========================

# =========================
# jobs
# send_data = {
#     "table": "jobs",
#     "job_id": 7,
#     "user_id": 3,
#     "title": "EE engineer",
#     "employment_type": "full-time",
#     "applicants": 5,
#     "description": "這份工作，需要做",
#     "qualifications_skills": "python-精通",
#     "hourSalary": 180,
#     "daySalary": 180*8,
#     "monthSalary": 180*8*30,
#     "yearSalary": 180*8*30*12,
#     "place": "台北市",
#     "phone": "0912345678"
# }
# modify
send_data = {"table": "jobs", "job_id": 6, "applicants": 0}
# =========================
# =========================
# applys
#     company, user
#     Confirm, Reject, No reply
# send_data = {
#     "table": "applys",
#     "user_id": 2,
#     "job_id": 7,
#     "originate": "user",
#     "status": "Reject"
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

# send_data = {'user_id': 3, 'title': 'ME engineer'}
send_data_json = json.dumps(send_data)
r = requests.post(url + 'add_to_table', json=send_data_json)

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
