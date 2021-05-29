from sqlalchemy import Column, Integer, String

from backend.entity.Base import Base


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
