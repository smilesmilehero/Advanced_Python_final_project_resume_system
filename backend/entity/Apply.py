from sqlalchemy import Column, Integer, PrimaryKeyConstraint

from backend.entity.Base import Base


class Apply(Base):
    __tablename__ = "applys"

    user_id = Column('user_id', Integer, index=True)
    job_id = Column('job_id', Integer, index=True)
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'job_id'),
    )

    def to_dict(self) -> dict:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
