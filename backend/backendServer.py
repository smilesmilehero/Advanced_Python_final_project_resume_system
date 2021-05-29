import logging
from datetime import datetime

from threading import Thread
from typing import Optional

# sqlalchemy import
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import scoped_session, sessionmaker

# DB import
from backend.entity.Base import Base
from backend.reop.ResumeRepo import ResumeRepo
from backend.reop.JobRepo import JobRepo
from backend.reop.UserRepo import UserRepo
from backend.reop.ApplyRepo import ApplyRepo
from backend.reop.CompanyRepo import CompanyRepo

from backend.service.Service import Service

from backend.api.UserApi import UserApi

# flask import
from flask import Flask
from waitress import serve


class BackendServer(Thread):
    def __init__(self, db_url: str, host: str, port: str):
        super().__init__()
        self.db_url = db_url
        self.host = host
        self.port = port

        self.engine: Optional[Engine] = None
        self.session: Optional[scoped_session] = None
        self.resume_repo: Optional[ResumeRepo] = None
        self.job_repo: Optional[JobRepo] = None
        self.user_repo: Optional[UserRepo] = None
        self.apply_repo: Optional[ApplyRepo] = None
        self.company_repo: Optional[CompanyRepo] = None

    def serve(self):
        logging.debug("start")
        self.start()

    def info(self):
        return "OK", 200

    def run(self):
        self.init_db()
        self.init_flask()
        logging.info('Backend Server Starting...')
        serve(self.app, host=self.host, port=self.port)

    def init_db(self):
        # self.engine = create_engine(self.db_url)
        logging.info('DB Initializing...')
        self.engine = create_engine(self.db_url, echo=True)
        session_factory = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.session = scoped_session(session_factory)
        self.resume_repo = ResumeRepo(session=self.session)
        self.job_repo = JobRepo(session=self.session)
        self.user_repo = UserRepo(session=self.session)
        self.apply_repo = ApplyRepo(session=self.session)
        self.company_repo = CompanyRepo(session=self.session)

    def init_flask(self):
        logging.info('Flask Initializing...')
        self.app = Flask(__name__)
        self.service = Service(user_repo=self.user_repo, resume_repo=self.resume_repo, company_repo=self.company_repo,
                               job_repo=self.job_repo, apply_repo=self.apply_repo)
        self.app.add_url_rule("/info", methods=["GET"], view_func=self.info)

        self.user_api = UserApi(app=self.app, service=self.service)

    def __str__(self):
        return "{}(db_url={}, resume_repo={}, job_repo={}, user_repo={}, apply_repo={}, company_repo={})".format(
            self.db_url, self.resume_repo, self.job_repo, self.user_repo, self.apply_repo, self.company_repo)

    def test_function(self):
        logging.info('Test function')
        user_data = {'account': 'sadgfsdg', 'password': 'jjjj', 'iscompany': False}
        user_search_cond = {'job_id': 2}
        resume_data = {'user_id': 2, 'name': 'kevin.jk', 'address': 'taiwan', 'phone': '0912345678',
                       'email': 'kevin@gmail',
                       'education': 'master', 'school': 'Taipei TECH', 'skill': 'python, medium\n eng, mid',
                       'profile': 'I am an experienced joiner with well developed skills and experience in groundwork, concrete finishing and steel fixing and have worked in the construction industry since 1982. I am also a skilled labourer who has supported many different trades over the years. I have a full clean UK driving licence with entitlement of up to 7.5 tonne. I am keen to return to work after a period of training and personal development which has broadened my skills and experiences.'}
        job_data = {'user_id': 2, 'job_id': 1, 'title': 'Intern', 'employment_type': '??df', 'applicants': 10,
                    'description': 'dkdkdv sdksf sf', 'responsibilities': 'jfkdsal asdf',
                    'qualifications_skills': 'askjfaldsjf ajdsk l', 'post_time': datetime.now()}
        # apply_data = {'user_id': 1, 'job_id': 2}
        account_name = 'jerry12zdg3'
        company_data = {'user_id': 3, 'name': 'kevin.jk', 'address': 'taiwan', 'phone': '0912345678',
                        'email': 'kevin@gmail', 'employees': '20', 'description': 'sjsvjs jdsfksdiv ksfjkdsa adkjf'}
        # res = self.service.data_merge('applys', apply_data)  # merge test
        res = self.service.data_search('applys', user_search_cond)  # search test
        # res = self.service.data_del('jobs', user_search_cond)  # search test
        print(res)

# if __name__ == "__main__":
#     BackendServer().run()
#     BackendServer.test_function()
