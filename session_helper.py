from config import Config
import qi

class SessionHelper:
    def __init__(self):
        pass

    @staticmethod
    def get_active_session():
        session = qi.Session()
        session.connect("tcp://" + Config().ip)

        return session

if __name__ == "__main__":
    session = SessionHelper.get_active_session()
    print("")
