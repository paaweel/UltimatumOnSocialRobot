import sqlite3
import logging
import os.path
import pandas as pd
from pandas import DataFrame


class DbConnector:
    def __init__(self):
        self.dbName = "ultiatumGame.db"
        connectionString = sqlite3.connect(self.dbName)
        self.connector = connectionString.cursor()
        if not os.path.isfile(self.dbName):
            logging.debug("Creating a new database")
            # create table for videoModule:
            self.connector.execute(
                """CREATE TABLE VIDEO_EMOTIONS
                                ([generated_id] INTEGER PRIMARY KEY,[timestamp] DATETIME,[emotionNumLabel] SMALLINT,[emotionLabel] TEXT,[certainty] REAL)"""
            )
            self.connector.execute(
                """CREATE TABLE ULTIMATUM_GAME
                                ([generated_id] INTEGER PRIMARY KEY,[gameId] INTEGER,[startTime] DATETIME,[roundId] SMALLINT,[humanOffer] SMALLINT,[robotDecision] BOOLEAN,[robotOffer] SMALLINT,[humanDecision] BOOLEAN,[humanScore] INTEGER,[robotScore] INTEGER)"""
            )
            self.connector.commit()
            logging.debug("Commiting changes to the database")

    def importCsv2Db(csvPath, tableName, ifExists="append"):
        logging.debug("Reading data from csv " + csvPath)
        readTableData = pd.read_csv(csvPath)
        readTableData.to_sql(tableName, self.connector, if_exists="append", index=False)
        logging.debug("Updated data with csv in table " + tableName)

    def exportDb2Csv(csvPath, tableName):
        logging.debug("Reading data from table " + tableName)
        df = pd.read_sql_query("SELECT * FROM " + tableName, self.connector)
        df.to_csv(csvPath, index=False)
        logging.debug("Exported data to csv from table " + tableName)


if __name__ == "__main__":
    logging.basicConfig(filename="logs/videoModule.log", level=logging.DEBUG)
    logging.debug("Starting database module")
    db = DbConnector()
    logging.debug("Exitting database module")
