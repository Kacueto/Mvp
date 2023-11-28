

import mysql.connector

from decouple import config
import mysql.connector

class DB:
    config={}
    def __init__(self):
        self.config['MYSQL_USER'] = config('MYSQL_USER')
        self.config['MYSQL_PASSWORD'] = config('MYSQL_PASSWORD')
        self.config['MYSQL_HOST'] = config('MYSQL_HOST') 
        self.config['MYSQL_DB'] = config('MYSQL_DATABASE')
        

    def get_db(self):
        return mysql.connector.connect(
            user=self.config['MYSQL_USER'],
            password=self.config['MYSQL_PASSWORD'],
            host=self.config['MYSQL_HOST'],
            database=self.config['MYSQL_DB'],
            
        )

    def close_db(self):
        db = self.config['db']
        if db is not None:
            db.close()

