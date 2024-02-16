import mysql.connector
import threading
import sqlite3
import time

def newDB(type, hostorfilename, port = 3306, username = '', password = '', database = ''):
    if type == 'SQLITE':
        return SQLite(hostorfilename)
    if type == 'MYSQL':
        return MYSQLDB(hostorfilename, port, username, password, database)
    
class MYSQLDB():
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


    def execute(self, statement):
        db, crs = self.connect()
        crs.execute(statement)
        res = crs.fetchall()
        self.close(db,crs)
        return res

    def close(self, db, crs):
        crs.close()
        db.close()

class SQLite(threading.Thread):
    def __init__(self, filename):  
        print("Initializing sqLite") 
        threading.Thread.__init__(self)
        self.filename = filename
        self.con = sqlite3.connect(self.filename, check_same_thread=False)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        self.queueid = 0
        self.queue = {}
        self.results = {}
        self.timeout = 10
        self.sleep = .01
        self.start()

    def run(self):
        while True:
            if len(self.queue) > 0:
                queue = self.queue.copy()
                for queryident in queue:
                    try:
                        self.results[queryident] = []
                        res = self.cur.execute(queue[queryident])
                        self.con.commit()
                        for r in res.fetchall():
                            self.results[queryident].append(dict(r))
                    except:
                        self.results[queryident] = False
                        pass
                    del self.queue[queryident]
            time.sleep(self.sleep)

    def execute(self, query):
        timeout = self.timeout
        self.queueid += 1
        self.queryident = 'Q_' + str(self.queueid)
        self.queue[self.queryident] = query
        while not self.queryident in self.results:
            timeout -= self.sleep
            if timeout <= 0: break
            time.sleep(self.sleep)
        if self.queryident in self.results:
            result = self.results[self.queryident]
            del self.results[self.queryident]
        else:
            result = False
        return result
