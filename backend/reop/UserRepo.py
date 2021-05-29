import logging

from backend.entity.User import User

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

class UserRepo:
    def __init__(self, session):
        self.session = session

    def _merge(self, user):
        with self.session() as session, session.begin():
            session.merge(User(**user))

    def merge(self, user: dict):
        self._merge(user)

    def merge_all(self, user_data_list: list):
        for each_user_data in user_data_list:
            self._merge(each_user_data)

    def search_by_condition(self, column_dict: dict):
        with self.session() as session, session.begin():
            found_list = []
            found_row = session.query(User).filter_by(**column_dict).all()
            for each_row in found_row:
                found_list.append(each_row.to_dict())
            return found_list

    def del_by_condition(self, column_dict: dict):
        with self.session() as session, session.begin():
           session.query(User).filter_by(**column_dict).delete()


    def get_account_info_by_account(self, account_name):
        with self.session() as session, session.begin():
            found_row = session.query(User).filter_by(account=account_name).first()
            return found_row.to_dict()

    def check_account_exist(self, account_data):
        with self.session() as session, session.begin():
            data = session.query(User).filter_by(account=account_data).all()
            if len(data) > 0:
                return True
            else:
                return False

    def find_all(self) -> list:
        with self.session() as session, session.begin():
            user_list = []
            data = session.query(User).filter_by().all()
            for each_data in data:
                user_list.append(each_data.to_dict())
            return user_list

    def check_password(self, account_data) -> str:
        with self.session() as session, session.begin():
            data = session.query(User).filter_by(account=account_data).first()
            return data.password


