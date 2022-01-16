from pathprovider import PathProvider


class GameVersions:
    def __init__(self):
        pathProvider = PathProvider()

        self.general = pathProvider.topicDir + self.generalTopic
        self.emphatic = pathProvider.topicDir + self.emphaticTopic
        self.egoistic = pathProvider.topicDir + self.egoisticTopic
