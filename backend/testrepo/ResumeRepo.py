from creatDB import User

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine


class ResumeRepo:
    def __init__(self, session):
        self.session = session

    def _merge(self, user: dict):
        with self.session() as session, session.begin():
            session.merge(User(**user))

    def merge(self, user: dict):
        self._merge(user)


