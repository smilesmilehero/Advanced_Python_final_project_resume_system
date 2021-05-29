from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, PrimaryKeyConstraint
from sqlalchemy.orm import registry

mapper_reg = registry()
Base = mapper_reg.generate_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column('user_id', Integer, primary_key=True)
    account = Column('account', String, unique=True)
    password = Column('password', String)
    iscompany = Column('iscompany', Boolean)

    # __table_args__ = (
    #     PrimaryKeyConstraint('user_id', 'account'),
    # )

    def to_dict(self) -> dict:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Resume(Base):
    __tablename__ = "resumes"

    user_id = Column('user_id', Integer, primary_key=True)
    name = Column('name', String)
    address = Column('address', String)
    phone = Column('phone', String)
    email = Column('email', String)
    education = Column('education', String)
    school = Column('school', String)
    skill = Column('skill', String)
    profile = Column('profile', String)

    def to_dict(self) -> dict:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Company(Base):
    __tablename__ = "companys"

    user_id = Column('user_id', Integer, primary_key=True)
    name = Column('name', String)
    address = Column('address', String)
    phone = Column('phone', String)
    email = Column('email', String)
    employees = Column('employees', String)
    description = Column('description', String)

    def to_dict(self) -> dict:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Job(Base):
    __tablename__ = "jobs"

    user_id = Column('user_id', Integer)
    job_id = Column('job_id', Integer, primary_key=True)
    title = Column('title', String)
    employment_type = Column('employment_type', String)
    applicants = Column('applicants', Integer)
    description = Column('description', String)
    responsibilities = Column('responsibilities', String)
    qualifications_skills = Column('qualifications_skills', String)
    post_time = Column('post_time', DateTime, default=datetime.now)

    def to_dict(self) -> dict:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Apply(Base):
    __tablename__ = "applys"

    user_id = Column('user_id', Integer, index=True)
    job_id = Column('job_id', Integer, index=True)
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'job_id'),
    )

    def to_dict(self) -> dict:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


# engine = create_engine('postgresql://twjakjfu:XiIlyFJEk4NNUYj9GYjDGQ6MpZ9w2L6r@satao.db.elephantsql.com:5432/twjakjfu',
#                        echo=True)

if __name__ == "__main__":
    engine = create_engine('sqlite:///job_search_test.db', echo=True)
    Base.metadata.create_all(bind=engine)
