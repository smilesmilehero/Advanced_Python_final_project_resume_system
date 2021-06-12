from sqlalchemy import Column, Integer, String, Boolean

from backend.entity.Base import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column('user_id', Integer, primary_key=True)
    account = Column('account', String, unique=True)
    password = Column('password', String)
    iscompany = Column('iscompany', Boolean)

    def to_dict(self) -> dict:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
