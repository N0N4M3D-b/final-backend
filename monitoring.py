from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import Namespace
from enum import Enum
from initialize_database import connect_database
from initialize_database import disconnect_database
from login import VerifyJWT
import copy

Monitoring = Namespace('Monitoring')

class PageType(Enum):
    OOB = 40000
    SINGLE = 20000
    FIRST = 20001
    LAST = 20002
    MIDDLE = 20003
    NONE = 20004

    def __int__(self):
        return self.value

def checkPageType(table_flag, index):
    # out of boundary -> total < index
    # none page -> element zero
    # single page (0) -> total <= (10/5)
    # first page -> index == 1
    # last page -> total - index < (10/5)
    # middle page -> else
    
    if table_flag == 0:
        PAGE_MAX = 10
        query = f'SELECT COUNT(*) FROM UnsolvedCase'
    else:
        PAGE_MAX = 5
        query = f'SELECT COUNT(*) FROM SolvedCase'

    db, cursor = connect_database()
    
    cursor.execute(query)
    total = cursor.fetchone()[0]

    disconnect_database(db)

    if total == 0:
        return PageType.NONE
    elif index > total or index < 1:
        return PageType.OOB
    elif index == 1:
        if total <= PAGE_MAX:
            return PageType.SINGLE
        else:
            return PageType.FIRST
    elif total - index < PAGE_MAX:
        return PageType.LAST
    else:
        return PageType.MIDDLE

def isExistCaseNum(table_flag, caseNum):
    db, cursor = connect_database()

    if table_flag == 0:
        query = f'SELECT COUNT(*) FROM UnsolvedCase WHERE caseNum = {caseNum}'
    else:
        query = f'SELECT COUNT(*) FROM SolvedCase WHERE caseNum = {caseNum}'

    cursor.execute(query)
    total = cursor.fetchone()[0]

    disconnect_database(db)

    if total == 1:
        return True
    else:
        return False
    
def getCase(table_flag, index):
    db, cursor = connect_database()

    if table_flag == 0:
        query = f'SELECT * FROM UnsolvedCase ORDER BY detectedTime DESC LIMIT {index - 1}, 10'
    else:
        query = f'SELECT * FROM SolvedCase ORDER BY detectedTime DESC LIMIT {index - 1}, 5'

    cursor.execute(query)
    result = cursor.fetchall()

    disconnect_database(db)

    return result

def getCaseOne(table_flag, caseNum):
    db, cursor = connect_database()

    if table_flag == 0:
        query = f'SELECT * FROM UnsolvedCase WHERE caseNum = {caseNum}'
    else:
        query = f'SELECT * FROM SolvedCase WHERE caseNum = {caseNum}'

    cursor.execute(query)
    result = cursor.fetchone()

    disconnect_database(db)

    return result

def setCaseOne(table_flag, case_num_data, email=None, name=None, tel=None, new_case_flag=None):
    db, cursor = connect_database()
    
    if table_flag == 0 and new_case_flag == True:
        query = f'INSERT INTO UnsolvedCase VALUES (NULL, "{case_num_data[1]}", "{case_num_data[2]}", "{case_num_data[3]}", CURRENT_TIMESTAMP)'
    elif table_flag == 0:
        query = f'INSERT INTO SolvedCase VALUES ({case_num_data[0]}, "{case_num_data[1]}", "{case_num_data[2]}", "{case_num_data[3]}", "{case_num_data[4].strftime("%Y/%m/%d %H:%M:%S")}", CURRENT_TIMESTAMP, "{email}", "{name}", "{tel}")'
    else:
        query = f'INSERT INTO UnsolvedCase VALUES ({case_num_data[0]}, "{case_num_data[1]}", "{case_num_data[2]}", "{case_num_data[3]}", "{case_num_data[4].strftime("%Y/%m/%d %H:%M:%S")}")'

    cursor.execute(query)
    db.commit()

    disconnect_database(db)

def deleteCaseOne(table_flag, caseNum):
    db, cursor = connect_database()

    if table_flag == 0:
        query = f'DELETE FROM UnsolvedCase WHERE caseNum = {caseNum}'
    else:
        query = f'DELETE FROM SolvedCase WHERE caseNum = {caseNum}'

    cursor.execute(query)
    db.commit()

    disconnect_database(db)


@Monitoring.route('/unsolved/<int:index>')
class UnsolvedGet(Resource):
    @VerifyJWT
    def get(self, index):
        self.index = index
        pagetype = checkPageType(0, self.index)

        if pagetype == PageType.OOB:
            return {
                'message' : 'Invalid index value',
                'status' : int(PageType.OOB)
            }
        
        db_element = getCase(0, self.index)
        
        data = []

        for element in db_element:
            tmp_dict = {}
            tmp_dict["caseNum"] = element[0]
            tmp_dict["latitude"] = element[1]
            tmp_dict["longitude"] = element[2]
            tmp_dict["pic"] = element[3]
            tmp_dict["detectedTime"] = element[4].strftime("%Y/%m/%d %H:%M:%S")

            data.append(copy.deepcopy(tmp_dict))

        return {
            'data' : data,
            'message' : 'Get UnsolvedCase data success',
            'status' : int(pagetype)
        }


@Monitoring.route('/solved/<int:index>')
class SolvedGet(Resource):
    def get(self, index):
        self.index = index
        pagetype = checkPageType(1, self.index)

        if pagetype == PageType.OOB:
            return {
                'message' : 'Invalid index value',
                'status' : int(PageType.OOB)
            }
        
        db_element = getCase(1, self.index)
        
        data = []

        for element in db_element:
            tmp_dict = {}
            tmp_dict["caseNum"] = element[0]
            tmp_dict["latitude"] = element[1]
            tmp_dict["longitude"] = element[2]
            tmp_dict["pic"] = element[3]
            tmp_dict["detectedTime"] = element[4].strftime("%Y/%m/%d %H:%M:%S")
            tmp_dict["solvedTime"] = element[5].strftime("%Y/%m/%d %H:%M:%S")
            tmp_dict["email"] = element[6]
            tmp_dict["name"] = element[7]
            tmp_dict["tel"] = element[8]

            data.append(copy.deepcopy(tmp_dict))

        return {
            'data' : data,
            'message' : 'Get SolvedCase data success',
            'status' : int(pagetype)
        }

@Monitoring.route('/unsolved')
class UnSolved(Resource):
    def post(self):
        try:
            self.latitude = request.json.get('latitude')
            self.longitude = request.json.get('longitude')
            self.pic = request.json.get('pic')
        except:
            print('[!] /list/unsolved (POST) : Invalid request data')
            return {
                'message' : 'Invalid request data',
                'status' : 400
            }
        
        try:
            case_num_data = (None, self.latitude, self.longitude, self.pic)
            setCaseOne(0, case_num_data, new_case_flag=True)
        except:
            return {
                'message' : 'Database error',
                'status' : 400
            }
        return {
            'message' : 'Register unsolved case success',
            'status' : 200
        }

    def put(self):
        try:
            self.caseNum = int(request.json.get('caseNum'))
            self.email = request.json.get('email')
        except:
            print('[!] /list/unsolved (PUT) : Invalid request data')
            return {
                'message' : 'Invalid request data',
                'status' : 400
            }
        try:
            tmp = self.getUserNameTelByEmail()
            self.name = tmp[0]
            self.tel = tmp[1]
        except:
            return {
                'message' : 'Invalid user access',
                'status' : 40000
            } 
        
        if isExistCaseNum(0, self.caseNum) == False:
            return {
                'message' : 'Invalid case number',
                'status' : 40001
            }
        
        self.case_num_data = getCaseOne(0, self.caseNum)

        try:
            setCaseOne(0, self.case_num_data, self.email, self.name, self.tel)
            deleteCaseOne(0, self.caseNum)

            return {
                'message' : 'Move UnsolvedCase data to SolvedCase Success',
                'status' : 200
            }
        except:
            return {
                'message' : 'Database error',
                'status' : 400
            }
    
    def getUserNameTelByEmail(self):
        db, cursor = connect_database()

        query = f'SELECT name, tel FROM Profiles WHERE email = "{self.email}"'
        cursor.execute(query)
        result = cursor.fetchone()

        disconnect_database(db)

        return result
    

@Monitoring.route('/solved')
class Solved(Resource):
    def put(self):
        try:
            self.caseNum = int(request.json.get('caseNum'))
        except:
            print('[!] /list/solved (PUT) : Invalid request data')
            return {
                'message' : 'Invalid request data',
                'status' : 400
            }
        
        if isExistCaseNum(1, self.caseNum) == False:
            return {
                'message' : 'Invalid case number',
                'status' : 40000
            }
        
        self.case_num_data = getCaseOne(1, self.caseNum)

        try:
            setCaseOne(1, self.case_num_data)
            deleteCaseOne(1, self.caseNum)

            return {
                'message' : 'Move SolvedCase data to UnsolvedCase Success',
                'status' : 200
            }
        except:
            return {
                'message' : 'Database error',
                'status' : 400
            }

    def delete(self):
        try:
            self.caseNum = int(request.json.get('caseNum'))
        except:
            print('[!] /list/solved (DELETE) : Invalid request data')
            return {
                'message' : 'Invalid request data',
                'status' : 400
            }
        
        if isExistCaseNum(1, self.caseNum) == False:
            return {
                'message' : 'Invalid case number',
                'status' : 40000
            }
        
        deleteCaseOne(1, self.caseNum)

        return {
            'message' : 'Delete SolvedCase data Success',
            'status' : 200
        }