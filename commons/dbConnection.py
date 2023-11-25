

import mysql.connector

class DB:
    config={}
    def __init__(self):
        self.config['MYSQL_USER'] = 'root'
        self.config['MYSQL_PASSWORD'] = ''
        self.config['MYSQL_HOST'] = 'localhost' 
        self.config['MYSQL_DB'] = 'mvpbbd'
        

    def get_db(self):
        return mysql.connector.connect(
            user=self.config['MYSQL_USER'],
            password=self.config['MYSQL_PASSWORD'],
            host=self.config['MYSQL_HOST'],
            database=self.config['MYSQL_DB']
        )

    def close_db(self):
        db = self.config['db']
        if db is not None:
            db.close()

db_connection = DB().get_db()