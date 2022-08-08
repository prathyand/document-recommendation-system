import mysql.connector
from dotenv import load_dotenv
import os

class dbconnector:

    default_conf = {
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'host': os.environ['MYSQL_HOST'],
    'port': os.environ['MYSQL_PORT'],
    'database': os.environ['MYSQL_DATABASE'] ,
    'raise_on_warnings': True}

    cnx=None
    cursordb=None

    def __init__(self,config=None,buffered=True) -> None:
        load_dotenv()

        if not config:
            config = self.default_conf

        self.cnx = mysql.connector.connect(**config)
        self.cursordb = self.cnx.cursor(buffered=buffered)

    def get_cursor(self):
        return self.cursordb


    def close_cnx(self):
        self.cnx.commit()
        self.cnx.close()
        self.cursordb.close()
        
        