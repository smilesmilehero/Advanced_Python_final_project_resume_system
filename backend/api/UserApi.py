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
from backend.service.mail import send_mail

url = 'http://127.0.0.1:5000/'


class UserApi:

    def __init__(self, app: Flask, service):
        self.service = service
        # app.add_url_rule('/register_user_account', methods=['POST'], view_func=self.register_user_account)
        # app.add_url_rule('/register_jobs', methods=['POST'], view_func=self.register_jobs)
        app.add_url_rule('/add_to_table', methods=['POST'], view_func=self.add_to_table)
        app.add_url_rule('/search_from_table', methods=['POST'], view_func=self.search_from_table)
        app.add_url_rule('/check_password', methods=['POST'], view_func=self.check_password)
        # app.add_url_rule('/job_search', methods=['POST'], view_func=self.job_search)
        app.add_url_rule('/apply_search', methods=['POST'], view_func=self.apply_search)
        app.add_url_rule('/test_send_mail', methods=['POST'], view_func=self.test_send_mail)
        app.add_url_rule('/test_textSplit_complexSearch', methods=['POST'], view_func=self.test_textSplit_complexSearch)
        app.add_url_rule('/resume_textSplit_complexSearch', methods=['POST'], view_func=self.resume_textSplit_complexSearch)
        # app.add_url_rule('/contain_search', methods=['POST'], view_func=self.contain_search)
        app.add_url_rule('/test', methods=['POST'], view_func=self.test)

        # TODO
        pass

    def add_to_table(self):
        data = json.loads(request.get_json())
        table = data['table']
        data.pop('table')
        print(data)
        print("{} {}".format(data, type(data)))
        try:
            self.service.data_merge(table, data)
            status = "ok"
            description = "success"
        except Exception as e:
            status = "err"
            description = e
        return {"status": status, 'description': description}

    def search_from_table(self):
        data = json.loads(request.get_json())
        print("type", type(data), data)
        table = data['table']
        data.pop('table')
        print(data)
        try:
            rsp = self.service.data_search(table, data)
            print(rsp)
            if len(rsp['description']) > 0:
                status = 'OK'
                description = rsp['description']
            else:
                status = 'fail'
                description = 'not found'
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

        data = json.loads(request.get_json())
        print("data", data)
        rsp_job = self.service.data_search('jobs', data)
        print(rsp_job)
        if len(rsp_job["description"]) > 0:
            status = 'ok'
            description = rsp_job["description"]
            for i, item in enumerate(rsp_job["description"]):
                print('user_id=', type(item['user_id']))
                send_data = {
                    "user_id": item['user_id']
                    # "user_id": 3
                }
                print("send_data=", send_data)
                rsp_company = self.service.data_search('companys', send_data)
                print("rsp_company", rsp_company)
                for compant_info in rsp_company['description']:
                    description[i][compant_info] = rsp_company['description'][compant_info]

            print(description)

        else:
            status = 'fail'
            description = 'not found'
        return {"status": status, 'description': description}

    # def apply_add(self):
    #     data = json.loads(request.get_json())
    #     rsp = self.service.data_merge('applys', data)

    #     pass



#apply_search returns (apply info) ,(company info) and each (job info) of a certain user's applications  #
    def apply_search(self):                        
        data = json.loads(request.get_json())
        rsp_apply = self.service.data_search('applys', data)
        print('apply=',rsp_apply)
        if rsp_apply["status"] == 'ok':
            if len(rsp_apply["description"]) > 0:
                description=rsp_apply['description']
                for i, item in enumerate(rsp_apply["description"]):
                    send_data = {
                        "job_id": item['job_id']
                    }
                    print("send_data=", send_data)
                    rsp_job_info = self.service.data_search('jobs', send_data)
                    print('\n')
                    print("rsp_job_info=", rsp_job_info)
                    print('\n')
                    company_id=rsp_job_info['description'][0]['user_id']
                    rsp_job_info['description'][0].pop('user_id')
                    send_data = {
                        "user_id": company_id
                    }
                    rsp_company_info = self.service.data_search('companys', send_data)

                    for job_info in rsp_job_info['description'][0]:
                        description[i][job_info] = rsp_job_info['description'][0][job_info]
                    rsp_company_info['description'][0].pop('user_id')
                    for company_info in rsp_company_info['description'][0]:
                        description[i][company_info] = rsp_company_info['description'][0][company_info]

                return { 'status':'OK','description':description }
                
            else:
                return { 'status':'fail','description':'not found'}
                


    def contain_search(self,data):
        data = json.loads(request.get_json())
        print('data', data)
        rsp = self.service.contain_search('jobs', data, data['mode'])
        print('rsp', rsp)
        return rsp

    def test_send_mail(self):
        # V {"account": "jk@gmail"}
        data = json.loads(request.get_json())
        account_rsp = self.service.data_search('users', data)
        if account_rsp["status"] == 'ok':
            if len(account_rsp["description"]) > 0:
                password = account_rsp["description"][0]["password"]
                search_condition = {"user_id": account_rsp["description"][0]["user_id"]}
                if account_rsp["description"][0]["iscompany"]:
                    rsp_detail = self.service.data_search('companys', search_condition)
                else:
                    rsp_detail = self.service.data_search('resumes', search_condition)
                if rsp_detail["status"] == 'ok':
                    if len(rsp_detail["description"]) > 0:
                        communication_mail = rsp_detail["description"][0]["email"]
                        try:
                            send_mail(communication_mail, [data["account"], password])
                            status = 'ok'
                            description = 'send to {}'.format(communication_mail)
                        except Exception as e:
                            description = e
                else:
                    status = 'err'
                    description = 'detail sql search err'
            else:
                status = 'err'
                description = "Account not Found"
        else:
            status = 'err'
            description = 'account sql search err'
        return {"status": status, 'description': description}

    def test_salary_transform(self):
        # V input => {"text": "python", "user_id": 5, "place": "台北市", "salary": ["yearSalary", 1200000]}
        data = json.loads(request.get_json())
        data = self.salary_transform(data)
        print(data)
        return data

###
    def test_textSplit_complexSearch(self):
        # V input => {"text": "python matlab engineer", "place": "台北市", "salary": ["hourSalary", 190]}
        data = json.loads(request.get_json())
        salary_mode = data["salary"][0]
        price = data["salary"][1]
        data.pop('salary')
        # data = self.salary_transform(data)
        text_list = data["text"].split()  # 文字分割
        data.pop('text')
        job_rsp = self.service.search_by_text_column_dict_salary("jobs", data, text_list, salary_mode, price)
        if job_rsp['status'] == 'ok':
            for index, each_row in enumerate(job_rsp['description']):
                rsp_company = self.service.data_search('companys', {'user_id': each_row['user_id']})
                job_rsp['description'][index] = {**job_rsp['description'][index], **rsp_company['description'][0]}
                print(job_rsp['description'])
        else:
            print("job search err")
        return job_rsp

    def resume_textSplit_complexSearch(self):
        # V input => {"text": "python matlab engineer", "place": "台北市", "salary": ["hourSalary", 190]}
        data = json.loads(request.get_json())
        salary_mode = data["salary"][0]
        price = data["salary"][1]
        data.pop('salary')
        # data = self.salary_transform(data)
        text_list = data["text"].split()  # 文字分割
        data.pop('text')
        resume_rsp = self.service.search_by_text_column_dict_salary("resumes", data, text_list, salary_mode, price)
        if len(resume_rsp['description'])>0:
           return resume_rsp
        else:
            return {'status':'fail','descrition':'not found'}
        

    def test(self):
        data = json.loads(request.get_json())
        print('data', data)
        # text = data['text']
        # # 分段 list text_list
        # print('text', text)
        # data.pop('text')
        text_list = ['python', 'full-time']
        salary_mode = 'monthSalary'
        price = None
        rsp = self.service.search_by_text_column_dict_salary('jobs', data, text_list, salary_mode, price)
        # rsp = self.service.test('jobs', data)

        print('rsp', rsp)
        return {}

    def salary_transform(self, data: dict):
        try:
            ori_salary = data["salary"]
        except:
            return data
        data.pop("salary")
        salary_mode = ori_salary[0]
        salary = ori_salary[1]

        salary_dict = dict()
        if salary_mode == "yearSalary":
            base_salary = salary / 12 / 30 / 8
        elif salary_mode == "monthSalary":
            base_salary = salary / 30 / 8
        elif salary_mode == "daySalary":
            base_salary = salary / 8
        elif salary_mode == "hourSalary":
            base_salary = salary

        salary_dict["hourSalary"] = round(base_salary)
        salary_dict["daySalary"] = round(base_salary * 8)
        salary_dict["monthSalary"] = round(base_salary * 8 * 30)
        salary_dict["yearSalary"] = round(base_salary * 8 * 30 * 12)

        data = {**data, **salary_dict}  # 合併dict
        return data


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
