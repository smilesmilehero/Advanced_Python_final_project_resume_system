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
#     "account":"kevin@gmail.com",
#     "password":"123456",
#     "iscompany":False}
# send_data_json = json.dumps(send_data)
# r = requests.post(url + 'register_user_account', json=send_data_json)

# =========================

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
# send_data = {"table": "jobs", "job_id": 6, "applicants": 0}
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
# =========================
# salary transform
# send_data = {"text": "python", "user_id": 5, "place": "台北市", "salary": ["yearSalary", 1200000]}
# =========================
# =========================
# mail
# send_data = {"account": "google@gmail"}
# =========================
# =========================
# textSplit_complexSearch
# send_data = {"text": "python matlab engineer", "place": "台北市", "salary": ["hourSalary", 190]}
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
# send_data = {"table": "users", "user_id": 2}
# send_data = {"table": "companys", "user_id": 2}
# send_data = {'user_id': 3, 'title': 'ME engineer'}
# send_data = {'table': 'jobs', 'job_id': 2}
send_data={
            'job_id':9,
            'table':'applys'
        }
send_data_json=json.dumps(send_data)
rsp=requests.post(url+'delete',json=send_data_json)
rsp=json.loads(rsp.text)
print(rsp)
# print(r['description'][0]['post_time'])
# ts = r['description'][0]['post_time']
# from datetime import datetime
# format = '%a, %d %b %Y %H:%M:%S GMT'
# print(datetime.strptime(ts, format))

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


# =====================api test=========================
###job search###
# send_data = {
#     "employment_type":"full-time"
# }
# send_data_json = json.dumps(send_data)
# r = requests.post(url + 'job_search', json=send_data_json)
# r = json.loads(r.text)
# print(r)


###rigister user###
# iscompany = False
# send_data = {
#     "table":"users",
#     "account": 'an@gmail.com',
#     "password": '123456',
#     "iscompany": iscompany}
# send_data_json = json.dumps(send_data)
# r = requests.post(url + 'add_to_table', json=send_data_json)

###apply add###
# send_data = {
#     'table':'applys',
#     'user_id':3,
#     'job_id':6,
#     'originate':'user',
#     'status':'Confirm'
# }
# send_data_json = json.dumps(send_data)
# r = requests.post(url + 'add_to_table', json=send_data_json)

###search apply###
# send_data = {
#     'table':'applys',
#     'user_id':3,
# }
# send_data_json = json.dumps(send_data)
# r = requests.post(url + 'search_from_table', json=send_data_json)
# r = json.loads(r.text)
# print(r)


###user apply search ###

# send_data={
#     'user_id':1
# }
# data_json = json.dumps(send_data)
# r = requests.post(url + 'apply_search', json=data_json)
# r = json.loads(r.text)
# for item in r['description']:

#     print(item)


####resume search####

# send_data={"text": "python matlab engineer", "place": "台北市", "salary": ["hourSalary", 190]}
# data_json = json.dumps(send_data)
# r = requests.post(url + 'resume_textSplit_complexSearch', json=data_json)
# r = json.loads(r.text)
# print(r)


# send_data = {
#     'account': 'jk@gmail'
# }
# send_data = json.dumps(send_data)
#
# r = requests.post(url + 'send_mail', json=send_data)
#
# r = json.loads(r.text)
# print(r)

# send_data_json = json.dumps(send_data)
# print(type(send_data_json), send_data_json)
# r = requests.post(url + 'send_mail', json=send_data_json)
# r = json.loads(r.text)
