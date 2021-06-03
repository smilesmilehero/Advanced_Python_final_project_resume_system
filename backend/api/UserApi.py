from flask import Flask, request, jsonify

import sys

sys.path.append('/home/spie/Desktop/1092_Python_Object_Oriented/final')
print(sys.path)

from backend.reop.UserRepo import UserRepo
from backend.reop.ResumeRepo import ResumeRepo

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from backend.service import Service
import requests
import json

url = 'http://127.0.0.1:5000/'


class UserApi:

    def __init__(self, app: Flask, service):
        self.service = service
        app.add_url_rule('/register_user_account', methods=['POST'], view_func=self.register_user_account)
        app.add_url_rule('/register_jobs', methods=['POST'], view_func=self.register_jobs)
        app.add_url_rule('/check_password', methods=['POST'], view_func=self.check_password)
        app.add_url_rule('/job_search', methods=['POST'], view_func=self.job_search)
        app.add_url_rule('/apply_list', methods=['POST'], view_func=self.apply_list)

        app.add_url_rule('/contain_search', methods=['POST'], view_func=self.contain_search)
        app.add_url_rule('/test', methods=['POST'], view_func=self.test)

        # TODO
        pass

    def register_jobs(self):
        data = json.loads(request.get_json())
        print("{} {}".format(data, type(data)))
        try:
            self.service.data_merge('jobs', data)
            status = "ok"
            description = "success"
        except Exception as e:
            status = "err"
            description = e
        return {"status": status, 'description': description}

    def register_user_account(self):
        data = json.loads(request.get_json())
        print("{} {}".format(data, type(data)))
        try:
            self.service.data_merge('users', data)
            status = "ok"
            description = "success"
        except Exception as e:
            status = "err"
            description = e
        return {"status": status, 'description': description}

    def check_password(self):
        data = json.loads(request.get_json())
        rsp = self.service.data_search('users', data)
        if len(rsp["description"]) > 0:
            status = 'ok'
            description = {'user_id': rsp['description'][0]['user_id']}
        else:
            status = 'err'
            description = 'password error'
        return {"status": status, 'description': description}

    def job_search(self):
        print("sdfsd")

        data = json.loads(request.get_json())
        print("data", data)
        rsp = self.service.data_search('jobs', data)
        print(rsp)
        if len(rsp["description"]) > 0:
            status = 'ok'
            description = rsp["description"]
            for i, item in enumerate(rsp["description"]):
                print('user_id=', type(item['user_id']))
                send_data = {
                    #  "user_id":item['user_id']
                    "user_id": 3
                }
                print("send_data=", send_data)
                rsp2 = self.service.data_search('companys', send_data)
                print("rsp2=", rsp2)
                for compant_info in rsp2['description'][0]:
                    description[i][compant_info] = rsp2['description'][0][compant_info]

            print(description)

        else:
            status = 'err'
            description = 'password error'
        return {"status": status, 'description': description}

    def apply_list(self):
        pass

    def contain_search(self):
        data = json.loads(request.get_json())
        print('data', data)
        rsp = self.service.contain_search('jobs', data, data['mode'])
        print('rsp', rsp)
        return {}

    def test(self):
        data = json.loads(request.get_json())
        print('data', data)
        text = data['text']
        print('text', text)
        data.pop('text')
        rsp = self.service.test('jobs', data, text)
        print('rsp', rsp)
        return {}


if __name__ == "__main__":
    user_data = {'account': 'asdfads', 'password': 'jjjj', 'iscompany': False}
    user_search_cond = {'iscompany': True}

    resume_data = {'user_id': 2, 'name': 'kevin.jk', 'address': 'taiwan', 'phone': '0912345678', 'email': 'kevin@gmail',
                   'education': 'master', 'school': 'Taipei TECH', 'skill': 'python, medium\n eng, mid',
                   'profile': 'I am an experienced joiner with well developed skills and experience in groundwork, concrete finishing and steel fixing and have worked in the construction industry since 1982. I am also a skilled labourer who has supported many different trades over the years. I have a full clean UK driving licence with entitlement of up to 7.5 tonne. I am keen to return to work after a period of training and personal development which has broadened my skills and experiences.'}
    account_name = 'jerry12zdg3'
    engine = create_engine('sqlite:///job_search_test2.db', echo=True)
    session_factory = sessionmaker(bind=engine)
    session_1 = scoped_session(session_factory)
    user_repo = UserRepo(session=session_1)
    resume_repo = ResumeRepo(session=session_1)

    res = UserApi().add_new_account(user_data)
    print(res)

    # data = UserApi().get_account_data_by_account_name(account_name)
    # print(data)
    # UserApi().add_modify_resume(resume_data)

    # UserApi().user_search(user_search_cond)
