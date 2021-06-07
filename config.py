
class Config:
    def __init__(self):
        self.ip = '192.168.0.31'
        self.language = 'Polish'
        self.port = '9559'


if __name__ == "__main__":
    print(Config().ip)