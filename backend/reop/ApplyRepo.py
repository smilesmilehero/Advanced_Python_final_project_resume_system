from backend.entity.Apply import Apply


class ApplyRepo:
    def __init__(self, session):
        self.session = session

    def _merge(self, resume: dict):
        with self.session() as session, session.begin():
            session.merge(Apply(**resume))

    def merge(self, resume: dict):
        self._merge(resume)

    def search_by_condition(self, column_dict: dict):
        with self.session() as session, session.begin():
            found_list = []
            found_row = session.query(Apply).filter_by(**column_dict).all()
            for each_row in found_row:
                found_list.append(each_row.to_dict())
            return found_list

    def del_by_condition(self, column_dict: dict):
        with self.session() as session, session.begin():
           session.query(Apply).filter_by(**column_dict).delete()
