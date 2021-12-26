from config import Config
import qi
import logging


class SessionHelper:
    def __init__(self):
        pass

    @staticmethod
    def get_active_session():

        try:
            session = qi.Session()
            session.connect("tcp://" + Config().ip)

            return session
        except:
            logging.error("Unable to create seesion object")
        finally:
            return None


if __name__ == "__main__":
    session = SessionHelper.get_active_session()
    if session is not None:
        logging.info("Session sucessfuly established")
