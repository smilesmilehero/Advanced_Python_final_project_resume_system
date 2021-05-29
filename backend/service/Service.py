import logging

from backend.reop.UserRepo import UserRepo
from backend.reop.ResumeRepo import ResumeRepo
from backend.reop.CompanyRepo import CompanyRepo
from backend.reop.JobRepo import JobRepo
from backend.reop.ApplyRepo import ApplyRepo


class Service:
    def __init__(self, user_repo: UserRepo, resume_repo: ResumeRepo, company_repo: CompanyRepo, job_repo: JobRepo,
                 apply_repo: ApplyRepo):
        self.user_repo = user_repo
        self.resume_repo = resume_repo
        self.company_repo = company_repo
        self.job_repo = job_repo
        self.apply_repo = apply_repo
        logging.info("{}".format(self))

    def check_account_exist(self, account_name):
        return self.user_repo.check_account_exist(account_name)

    def add_new_account(self, account_info: dict):
        if self.check_account_exist(account_info['account']):
            res = {'status': 'err', 'description': 'account existed'}
        else:
            res = {'status': 'ok', 'description': 'account created'}
            self.user_repo.merge(account_info)
        return res

    # merge =======
    def data_merge(self, table: str, info_dict: dict):
        tables = {'users': self.user_repo,
                  'resumes': self.resume_repo,
                  'companys': self.company_repo,
                  'jobs': self.job_repo,
                  'applys': self.apply_repo}
        try:
            tables[table].merge(info_dict)
            res = {'status': 'ok', 'description': info_dict}
        except Exception as e:
            res = {'status': 'err', 'description': e}
        return res

    # def user_merge(self, info_dict: dict):
    #     try:
    #         self.user_repo.merge(info_dict)
    #         res = {'status': 'ok', 'description': info_dict}
    #     except Exception as e:
    #         res = {'status': 'err', 'description': e}
    #     return res
    #
    # def resume_merge(self, info_dict: dict):
    #     # TODO
    #     pass
    #
    # def company_merge(self, info_dict: dict):
    #     # TODO
    #     pass
    #
    # def job_merge(self, info_dict: dict):
    #     # TODO
    #     pass
    #
    # def apply_merge(self, info_dict: dict):
    #     # TODO
    #     pass

    # search =======
    def data_search(self, table: str, column: dict):
        tables = {'users': self.user_repo,
                  'resumes': self.resume_repo,
                  'companys': self.company_repo,
                  'jobs': self.job_repo,
                  'applys': self.apply_repo}
        try:
            found_data = tables[table].search_by_condition(column)
            res = {'status': 'ok', 'description': found_data}
        except Exception as e:
            res = {'status': 'err', 'description': e}
        return res

    # def user_search(self, column: dict):
    #     found_data = self.user_repo.search_by_condition(column)
    #     return found_data
    #
    # def resume_search(self, column: dict):
    #     # TODO
    #     pass
    #
    # def company_search(self, column: dict):
    #     # TODO
    #     pass
    #
    # def job_search(self, column: dict):
    #     # TODO
    #     pass
    #
    # def apply_search(self, column: dict):
    #     # TODO
    #     pass

    # del =======
    def data_del(self, table: str, column: dict):
        # TODO
        tables = {'users': self.user_repo,
                  'resumes': self.resume_repo,
                  'companys': self.company_repo,
                  'jobs': self.job_repo,
                  'applys': self.apply_repo}
        try:
            tables[table].del_by_condition(column)
            res = {'status': 'ok', 'description': dict(table=table, column=column)}
        except Exception as e:
            res = {'status': 'err', 'description': e}
        return res

    # def user_del(self, column: dict):
    #     # TODO
    #     pass
    #
    # def resume_del(self, column: dict):
    #     # TODO
    #     pass
    #
    # def company_del(self, column: dict):
    #     # TODO
    #     pass
    #
    # def job_del(self, column: dict):
    #     # TODO
    #     pass
    #
    # def apply_del(self, column: dict):
    #     # TODO
    #     pass
