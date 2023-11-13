import pymysql

CREATE_WHITELIST_TABLE = '''CREATE TABLE WhiteList (
    email varchar(45) PRIMARY KEY
)'''

CREATE_PROFILES_TABLE = '''CREATE TABLE Profiles (
    email varchar(45) NOT NULL PRIMARY KEY,
    name varchar(45) NOT NULL,
    password varchar(20) NOT NULL,
    tel varchar(13) NOT NULL
)'''

CREATE_UNSOLVEDCASE_TABLE = '''CREATE TABLE UnsolvedCase (
    caseNum int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    latitude varchar(9) NOT NULL,
    longitude varchar(9) NOT NULL,
    pic varchar(32) NOT NULL,
    detectedTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
)
'''

CREATE_SOLVEDCASE_TABLE = '''CREATE TABLE SolvedCase (
    caseNum int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    latitude varchar(9) NOT NULL,
    longitude varchar(9) NOT NULL,
    pic varchar(32) NOT NULL,
    detectedTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    solvedTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    email varchar(45) NOT NULL,
    name varchar(20) NOT NULL,
    tel varchar(13) NOT NULL
)
'''

queries = (CREATE_WHITELIST_TABLE, CREATE_PROFILES_TABLE, CREATE_UNSOLVEDCASE_TABLE, CREATE_SOLVEDCASE_TABLE)

class InitializeDatabase:
    def __init__(self):
        self.CreateTable()
        self.conn.close()

    def CreateTable(self):
        self.conn = pymysql.connect(host='database', user='finaluser', password='dongafinal1234!', db='final', charset='utf8')
        self.cursor = self.conn.cursor()

        for query in queries:
            try:
                self.cursor.execute(query)
            except:
                continue

def connect_database():
    db = pymysql.connect(host='database',
        port=3306,
        user='finaluser',
        passwd='dongafinal1234!',
        db='final',
        charset='utf8'
    )
    cursor = db.cursor()

    return db, cursor

def disconnect_database(db):
    db.close()