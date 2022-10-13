import sqlite3


class DB:
    def __init__(self):
        self.connection = sqlite3.connect('pass.db')
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute(
            '''CREATE TABLE userinfo (uname, email, site, password)''')
        self.connection.commit()

    def create_table2(self):
        self.cursor.execute(
            '''CREATE TABLE logininfo (name, password)''')
        self.connection.commit()

    def close_db(self):
        self.connection.close()
