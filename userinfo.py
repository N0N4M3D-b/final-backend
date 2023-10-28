from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import Namespace
from flask_restx import reqparse
from initialize_database import connect_database
from initialize_database import disconnect_database

Userinfo = Namespace('Userinfo')

@Userinfo.route('')
class Myinfo(Resource):
    def post(self):
        # Parse request arguments
        try:
            self.email = request.json.get('email')
        except:
            print('[!] /myinfo (POST) : Invalid request data')
            return {
                'message' : 'Invalid request data',
                'status' : 400
            }

        success, name, tel = self.getUserInfo()

        if success:
            return {
                'name' : name,
                'tel' : tel,
                'message' : 'success',
                'status' : 200
            }
        else:
            return {
                'message' : 'Invalid user info',
                'status' : 40000
            }

    def delete(self):
        # Parse request arguments
        try:
            self.email = request.json.get('email')
        except:
            print('[!] /myinfo (DELETE) : Invalid request data')
            return {
                'message' : 'Invalid request data',
                'status' : 400
            }

        success = self.deleteUser()

        if success:
            return {
                'message' : 'user delete success',
                'status' : 200
            }
        else:
            return {
                'message' : 'Invalid user info',
                'status' : 40000
            }

    def put(self):
        # Parse request arguments
        try:
            self.email = request.json.get('email')
            self.old = request.json.get('old')
            self.new = request.json.get('new')
        except:
            print('[!] /myinfo (PUT) : Invalid request data')
            return {
                'message' : 'Invalid request data',
                'status' : 400
            }

        success = self.changePassword()

        if success:
            return {
                'message' : 'change password success',
                'status' : 200
            }
        else:
            return {
                'message' : 'change password fail',
                'status' : 40001
            }

    
    def getUserInfo(self):
        db, cursor = connect_database()
        query = f'SELECT name, tel FROM Profiles WHERE email="{self.email}"'

        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            return False, None, None
        
        name, tel = result[0]

        disconnect_database(db)

        return True, name, tel

    
    def deleteUser(self):
        db, cursor = connect_database()
        query = f'SELECT * from Profiles WHERE email="{self.email}"'
        cursor.execute(query)

        user_info = cursor.fetchall()

        if len(user_info) == 0:
            return False

        user_info = user_info[0]

        query = f'DELETE FROM Profiles WHERE email="{self.email}"'
        cursor.execute(query)

        query = f'INSERT INTO DeletedProfiles VALUES ("{user_info[0]}", "{user_info[1]}", "{user_info[2]}", "{user_info[3]}")'
        cursor.execute(query)

        db.commit()

        disconnect_database(db)

        return True

    
    def changePassword(self):
        db, cursor = connect_database()
        query = f'SELECT 1 from Profiles WHERE email="{self.email}" AND password="{self.old}"'
        cursor.execute(query)

        is_valid = len(cursor.fetchall()) != 0

        if not is_valid:
            return False

        query = f'UPDATE Profiles SET password="{self.new}" WHERE email="{self.email}"'

        try:
            cursor.execute(query)
        except:
            db.rollback()
            raise

        db.commit()

        disconnect_database(db)

        return True