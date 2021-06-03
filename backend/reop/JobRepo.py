from backend.entity.Job import Job
from sqlalchemy import or_, and_


class JobRepo:
    def __init__(self, session):
        self.session = session

    def _merge(self, resume: dict):
        with self.session() as session, session.begin():
            session.merge(Job(**resume))

    def merge(self, resume: dict):
        self._merge(resume)

    def search_by_condition(self, column_dict: dict):
        with self.session() as session, session.begin():
            found_list = []
            found_row = session.query(Job).filter_by(**column_dict).all()
            for each_row in found_row:
                found_list.append(each_row.to_dict())
            return found_list

    def del_by_condition(self, column_dict: dict):
        with self.session() as session, session.begin():
            session.query(Job).filter_by(**column_dict).delete()

    def contain_search_by_condition(self, column_dict: dict, mode: str):
        with self.session() as session, session.begin():
            found_list = []
            command_list = []
            for key, value in column_dict.items():
                if key == "title":
                    command_list.append(Job.title.contains(value))
                elif key == "employment_type":
                    command_list.append(Job.employment_type.contains(value))
                elif key == "applicants":
                    command_list.append(Job.applicants.contains(value))
                elif key == "description":
                    command_list.append(Job.description.contains(value))
                elif key == "qualifications_skills":
                    command_list.append(Job.qualifications_skills.contains(value))
                elif key == "place":
                    command_list.append(Job.place.contains(value))

            if mode == 'and':
                found_row = session.query(Job).filter(and_(*command_list))
            else:
                found_row = session.query(Job).filter(or_(*command_list))
            for each_row in found_row:
                found_list.append(each_row.to_dict())
            return found_list

    def search_by_condition_or_version(self, column_dict: dict):
        with self.session() as session, session.begin():
            found_list = []
            command_list = []
            for col, value in column_dict.items():
                command_list.append(eval("Job.{}.contains('{}')".format(col, value)))
            found_row = session.query(Job).filter(or_(*command_list)).all()

            for each_row in found_row:
                found_list.append(each_row.to_dict())
            return found_list

    def search_by_text_column_dict_salary(self, column_dict: dict, text_list: list, salary_mode: str, price: int):
        with self.session() as session, session.begin():
            found_list = []
            command_list = []
            col_list = [col.name for col in Job.__table__.columns]
            for value in text_list:
                for key in col_list:
                    command_list.append(eval("Job.{}.contains('{}')".format(key, value)))

            if price == None:
                found_row = session.query(Job).filter_by(**column_dict).filter(or_(*command_list)).all()
            else:
                found_row = session.query(Job).filter_by(**column_dict).filter(or_(*command_list)).filter(
                    eval("Job.{} >= {}".format(
                        salary_mode, price))).all()
            for each_row in found_row:
                found_list.append(each_row.to_dict())
            return found_list

    def test(self, column_dict, text_list):
        with self.session() as session, session.begin():
            found_list = []
            found_row = session.query(Job).filter(Job.monthSalary >= 38000).all()
            for each_row in found_row:
                found_list.append(each_row.to_dict())
            return found_list
