from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import Namespace
from enum import Enum
from initialize_database import connect_database
from initialize_database import disconnect_database
import copy

Monitoring = Namespace('Monitoring')

class PageType(Enum):
    OOB = 40000
    SINGLE = 20000
    FIRST = 20001
    LAST = 20002
    MIDDLE = 20003

    def __int__(self):
        return self.value

def isExistCaseNum(table_name, caseNum):
    db, cursor = connect_database()

    query = f'SELECT COUNT(*) FROM {table_name} WHERE caseNum = {caseNum}'
    cursor.execute(query)
    total = cursor.fetchone()[0]

    disconnect_database(db)

    if total == 1:
        return True
    else:
        return False

@Monitoring.route('/unsolved/<int:index>')
class UnsolvedGet(Resource):
    def get(self, index):
        self.index = index
        pagetype = self.checkPageType()

        if pagetype == PageType.OOB:
            return {
                'message' : 'Invalid index value',
                'status' : int(PageType.OOB)
            }
        
        db_element = self.getUnsolvedCase()
        
        data = []

        for element in db_element:
            tmp_dict = {}
            tmp_dict["caseNum"] = element[0]
            tmp_dict["latitude"] = element[1]
            tmp_dict["longitude"] = element[2]
            tmp_dict["pic"] = element[3]
            tmp_dict["detectedTime"] = db_element[0][4].strftime("%Y/%m/%d %H:%M:%S")

            data.append(copy.deepcopy(tmp_dict))

        return {
            'data' : data,
            'message' : 'Get UnsolvedCase data success',
            'status' : int(pagetype)
        }

    def checkPageType(self):
        # out of boundary -> total < index
        # single page (0) -> total <= 10
        # first page -> index == 1
        # last page -> total - index < 10
        # middle page -> else

        db, cursor = connect_database()

        query = f'SELECT COUNT(*) FROM UnsolvedCase'
        cursor.execute(query)
        total = cursor.fetchone()[0]

        disconnect_database(db)

        if self.index > total or self.index < 1:
            return PageType.OOB
        elif self.index == 1:
            if total <= 10:
                return PageType.SINGLE
            else:
                return PageType.FIRST
        elif total - self.index < 10:
            return PageType.LAST
        else:
            return PageType.MIDDLE
        
    def getUnsolvedCase(self):
        db, cursor = connect_database()

        query = f'SELECT * FROM UnsolvedCase ORDER BY detectedTime DESC LIMIT {self.index - 1}, 10'
        cursor.execute(query)
        result = cursor.fetchall()

        disconnect_database(db)

        return result


@Monitoring.route('/solved/<int:index>')
class SolvedGet(Resource):
    def get(self, index):
        pass

@Monitoring.route('/unsolved')
class UnSolved(Resource):
    def post(self):
        try:
            self.latitude = request.json.get('latitude')
            self.longitude = request.json.get('longitude')
            self.pic = request.json.get('pic')
        except:
            print('[!] /unsolved (POST) : Invalid request data')
            return {
                'message' : 'Invalid request data',
                'status' : 400
            }
        
        try:
            self.UnsolvedInsertDatabase()
        except:
            return {
                'message' : 'Database error',
                'status' : 400
            }
        return {
            'message' : 'Register unsolved case success',
            'status' : 200
        }
        
    def UnsolvedInsertDatabase(self):
        db, cursor = connect_database()

        query = f'INSERT INTO UnsolvedCase VALUES (NULL, "{self.latitude}", "{self.longitude}", "{self.pic}", CURRENT_TIMESTAMP)'
        cursor.execute(query)
        db.commit()

        disconnect_database(db)

    def put(self):
        try:
            self.caseNum = int(request.json.get('caseNum'))
            self.email = request.json.get('email')
            #self.solvedTime = request.json.get('solvedTime')
        except:
            print('[!] /unsolved (PUT) : Invalid request data')
            return {
                'message' : 'Invalid request data',
                'status' : 400
            }
        try:
            self.name = self.getUserNameByEmail()
        except:
            return {
                'message' : 'Invalid user access',
                'status' : 40000
            } 
        
        if isExistCaseNum('UnsolvedCase', self.caseNum) == False:
            return {
                'message' : 'Invalid case number',
                'status' : 40001
            }
        
        self.case_num_data = self.getUnsolvedCaseOne()

        try:
            self.setSolvedCaseOne()
            self.deleteUnsolvedCaseOne()

            return {
                'message' : 'Move UnsolvedCase data to SolvedCase Success',
                'status' : 200
            }
        except:
            return {
                'message' : 'Database error',
                'status' : 400
            }
        
    def getUnsolvedCaseOne(self):
        db, cursor = connect_database()

        query = f'SELECT * FROM UnsolvedCase WHERE caseNum = {self.caseNum}'
        cursor.execute(query)
        result = cursor.fetchone()

        disconnect_database(db)

        return result
    
    def getUserNameByEmail(self):
        db, cursor = connect_database()

        query = f'SELECT name FROM Profiles WHERE email = "{self.email}"'
        cursor.execute(query)
        result = cursor.fetchone()[0]

        disconnect_database(db)

        return result
    
    def setSolvedCaseOne(self):
        db, cursor = connect_database()

        self.detected_time = self.case_num_data[4].strftime("%Y/%m/%d %H:%M:%S")
        
        query = f'INSERT INTO SolvedCase VALUES (NULL, "{self.case_num_data[1]}", "{self.case_num_data[2]}", "{self.case_num_data[3]}", "{self.name}", "{self.email}", "{self.detected_time}", CURRENT_TIMESTAMP)'
        cursor.execute(query)
        db.commit()

        disconnect_database(db)

    def deleteUnsolvedCaseOne(self):
        db, cursor = connect_database()

        query = f'DELETE FROM UnsolvedCase WHERE caseNum = {self.caseNum}'
        cursor.execute(query)
        db.commit()

        disconnect_database(db)

@Monitoring.route('/solved')
class Solved(Resource):
    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass