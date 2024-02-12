import mysql.connector

class DB():
    def __init__(self, host, port, username, password, database):  
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    def connect(self):
        db = mysql.connector.connect(
        host=self.host,
        user=self.username,
        password=self.password,
        database=self.database,
        port=self.port
        )

        return db, db.cursor(dictionary=True)


    def get(self, statement):
        db, crs = self.connect()
        crs.execute(statement)
        res = crs.fetchall()
        self.close(db,crs)
        return res

    def close(self, db, crs):
        crs.close()
        db.close()
