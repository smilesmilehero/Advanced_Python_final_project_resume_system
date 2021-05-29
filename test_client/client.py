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

send_data = {
    "title":"Intern",
    # "employment_type":"mange"
}
send_data_json = json.dumps(send_data)
r = requests.post(url + 'job_search', json=send_data_json)
r = json.loads(r.text)
print(r['description'])


# print("{} {} {}".format(r, type(r.text), r.text))
# r = json.loads(r.text)
# print(r['description'])