from config import Config
import qi
import logging


class SessionHelper:
    def __init__(self):
        pass

    @staticmethod
    def get_active_session():
        session = None
        try:
            session = qi.Session()
            session.connect(Config().fullIp)
        except:
            logging.error(f"Unable to create session object at ip:{Config().fullIp}")
        finally:
            return session


if __name__ == "__main__":
    session = SessionHelper.get_active_session()
    if session is not None:
        logging.info("Session sucessfuly established")
