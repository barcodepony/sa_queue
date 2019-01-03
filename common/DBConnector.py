import mysql.connector
from mysql.connector import Error
from common.SQL_CONSTANTS import *

class DBC(object):
    def __init__(self, host: str = GBL_HOST, port: int = GBL_PORT,
                 db: str = GBL_DB, user: str = GBL_USER, password: str = GBL_PASSWORD):
        self.host = host
        self.port = port
        self.db = db
        self.__user = user
        self.__password = password
        self.connection = None

    def connect(self):
        try:
            if isinstance(self.connection, mysql.connector.CMySQLConnection):
                if self.connection.is_connected():
                    print("reusing connection to SA")
                    return

            print("Building connection to SA")
            self.connection = mysql.connector.connect(host=self.host,
                                                      database=self.db,
                                                      port=self.port,
                                                      user=self.__user,
                                                      password=self.__password)
            if self.connection.is_connected():
                print("You are connected to SA")

        except Error as e:
            print("Error while connection to DB: ", e)

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            print("Disconnecting Database Connector")

    def __query_sql(self, sql):
        if self.connection is None:
            raise ConnectionError("Connection is not set.")
        if not self.connection.is_connected():
            raise ConnectionError("You are not connected to the DB!")

        cursor = self.connection.cursor()
        print("CALLING: %s" % sql)
        cursor.execute(sql)
        rec = cursor.fetchall()
        return rec

    def safe_execute_sql(self, sql:str):
        if not isinstance(sql, str):
            print("ERROR: Only accepting type of STR, not %s" % type(sql))
            return
        if sql.lower().__contains__("drop "):
            print("RESTRICTION: Cannot commit a SQL containing drop: %s" % sql)
            return
        self.__execute_sql(sql)

    def __execute_sql(self, sql:str):
        if self.connection is None:
            raise ConnectionError("Connection is not set.")
        if not self.connection.is_connected():
            raise ConnectionError("You are not connected to the DB!")
        cursor = self.connection.cursor()
        print("EXECUTING: %s" % sql)
        try:
            cursor.execute(sql)
        except Exception as e:
            print("Caught ERROR: %s" % sql)
        self.connection.commit()
