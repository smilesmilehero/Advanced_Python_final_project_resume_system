import logging

from creatDB import User

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine


class UserRepo:
    def __init__(self, session):
        self.session = session

    def _merge(self, user):
        with self.session() as session, session.begin():
            session.merge(User(**user))

    def merge(self, user: dict):
        # FIXME
        self._merge(user)

    def merge_all(self, user_data_list: list):
        for each_user_data in user_data_list:
            self._merge(each_user_data)

    def find_account_exist(self, account_data):
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


if __name__ == "__main__":
    try:
        user_list = [{'account': 'jerry123324', 'password': 'dfh2r', 'iscompany': False},
                     {'account': 'dfj23', 'password': 'jfjd', 'iscompany': False},
                     {'account': 'Google', 'password': 'gggg', 'iscompany': True}]
        user_data = {'account': 'jerry123', 'password': 'jjjj', 'iscompany': False}
        account_data = 'jerry123'
        engine = create_engine('sqlite:///job_search_test.db', echo=True)
        session_factory = sessionmaker(bind=engine)
        session_1 = scoped_session(session_factory)
        user_repo = UserRepo(session=session_1)

        # merge
        #     user_repo.merge(user_data)

        # merge_all
        user_repo.merge_all(user_list)

    # find_account_exist
    # is_exist = user_repo.find_account_exist(account_data)
    # print(is_exist)

    # find_all
    # all_user = user_repo.find_all()
    # for i in all_user:
    #     print(i)
    # print(all_user)

    # check_password
    # str_password = user_repo.check_password(account_data)
    # print(str_password)

    except Exception as e:
        print(e)
        if "UNIQUE constraint failed: users.account" in str(e):
            # print("Exception is =>>>", e)
            print("Account exist")
