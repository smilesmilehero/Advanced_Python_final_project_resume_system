from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from backend.entity.Base import Base


class Job(Base):
    __tablename__ = "jobs"
    print("Job_Load")

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