from backend.entity.Company import Company
from sqlalchemy import or_, and_


class CompanyRepo:
    def __init__(self, session):
        self.session = session

    def _merge(self, resume: dict):
        with self.session() as session, session.begin():
            session.merge(Company(**resume))

    def merge(self, resume: dict):
        self._merge(resume)

    def search_by_condition(self, column_dict: dict):
        print('column_dict', column_dict)
        with self.session() as session, session.begin():
            found_list = []
            found_row = session.query(Company).filter_by(**column_dict).all()
            for each_row in found_row:
                found_list.append(each_row.to_dict())
            print('fond_list', found_list)

            return found_list

    def del_by_condition(self, column_dict: dict):
        with self.session() as session, session.begin():
            session.query(Company).filter_by(**column_dict).delete()

    def contain_search_two_version(self, column_dict: dict, mode: str):
        with self.session() as session, session.begin():
            found_list = []
            command_list = []
            for col, value in column_dict.items():
                command_list.append(eval("Company.{}.contains('{}')".format(col, value)))

            if mode == 'or':
                found_row = session.query(Company).filter(or_(*command_list)).all()
            else:
                found_row = session.query(Company).filter(and_(*command_list)).all()

            for each_row in found_row:
                found_list.append(each_row.to_dict())
            return found_list

    def search_by_text_column_dict_salary(self, column_dict: dict, text_list: list, salary_mode: str, price: int):
        with self.session() as session, session.begin():
            found_list = []
            command_list = []
            col_list = [col.name for col in Company.__table__.columns]
            for value in text_list:
                for key in col_list:
                    command_list.append(eval("Company.{}.contains('{}')".format(key, value)))

            if price == None:
                found_row = session.query(Company).filter_by(**column_dict).filter(or_(*command_list)).all()
            else:
                found_row = session.query(Company).filter_by(**column_dict).filter(or_(*command_list)).filter(
                    eval("Company.{} >= {}".format(
                        salary_mode, price))).all()
            for each_row in found_row:
                found_list.append(each_row.to_dict())
            return found_list
