from backend.entity.Resume import Resume
from sqlalchemy import or_, and_


class ResumeRepo:
    def __init__(self, session):
        self.session = session

    def _merge(self, resume: dict):
        with self.session() as session, session.begin():
            session.merge(Resume(**resume))

    def merge(self, resume: dict):
        self._merge(resume)

    def search_by_condition(self, column_dict: dict):
        with self.session() as session, session.begin():
            found_list = []
            found_row = session.query(Resume).filter_by(**column_dict).all()
            for each_row in found_row:
                found_list.append(each_row.to_dict())
            return found_list

    def del_by_condition(self, column_dict: dict):
        with self.session() as session, session.begin():
           session.query(Resume).filter_by(**column_dict).delete()

    def contain_search_two_version(self, column_dict: dict, mode: str):
        with self.session() as session, session.begin():
            found_list = []
            command_list = []
            for col, value in column_dict.items():
                command_list.append(eval("Resume.{}.contains('{}')".format(col, value)))

            if mode == 'or':
                found_row = session.query(Resume).filter(or_(*command_list)).all()
            else:
                found_row = session.query(Resume).filter(and_(*command_list)).all()

            for each_row in found_row:
                found_list.append(each_row.to_dict())
            return found_list

    def search_by_text_column_dict_salary(self, column_dict: dict, text_list: list, salary_mode: str, price: int):
        with self.session() as session, session.begin():
            found_list = []
            command_list = []
            col_list = [col.name for col in Resume.__table__.columns]
            for value in text_list:
                for key in col_list:
                    command_list.append(eval("Resume.{}.contains('{}')".format(key, value)))

            if price == None:
                found_row = session.query(Resume).filter_by(**column_dict).filter(or_(*command_list)).all()
            else:
                found_row = session.query(Resume).filter_by(**column_dict).filter(or_(*command_list)).filter(
                    eval("Resume.{} <= {}".format(
                        salary_mode, price))).all()
            for each_row in found_row:
                found_list.append(each_row.to_dict())
            return found_list
