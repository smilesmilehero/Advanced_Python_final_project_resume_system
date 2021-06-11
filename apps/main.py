import sys
sys.path.append('/home/spie-lab-01/109-2 python/final project/job_system/Advanced_Python_final_project_resume_system')
# sys.path.append('/home/spie/PycharmProjects/Advanced_Python_final_project_resume_system_v2')

# print(sys.path)
import logging
from sqlalchemy import create_engine

# DB import
# from backend.entity.Base import Base
# from backend.reop.JobRepo import JobRepo
# from backend.reop.JobRepo import JobRepo
# from backend.reop.UserRepo import UserRepo
# from backend.reop.ApplyRepo import ApplyRepo
# from backend.reop.CompanyRepo import CompanyRepo

from backend.backendServer import BackendServer

if __name__ == "__main__":
    config = {
        "format":
            "[%(asctime)s][%(levelname)s][%(threadName)s][%(filename)s] %(funcName)s() %(message)s",
        "root": "INFO"
    }
    logging.basicConfig(format=config["format"], level=config["root"])
    logging.basicConfig(level=logging.INFO)

    host = '127.0.0.1'
    port = 5000

    # logging.error("start----")
    # logging.warning("debug")
    # logging.info("debug")
    # logging.debug("debug")

    db_url = 'sqlite:///job_search.db'

    engine = create_engine(db_url, echo=True)
    # Base.metadata.create_all(bind=engine)
    backend_server = BackendServer(db_url=db_url, host=host, port=port)
    # backend_server.setDaemon(True)
    backend_server.run()
    backend_server.test_function()
