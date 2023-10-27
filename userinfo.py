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

        try:
            name, tel = self.getUserInfo()
        except:
            return {
                'message' : 'Invalid user info',
                'status' : 40000
            }

        return {
            'name' : name,
            'tel' : tel,
            'message' : 'success',
            'status' : 200
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

        result = self.deleteUser()

        if result:
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

        try:
            result = self.changePassword()
        except:
            return {
                'message' : 'Invalid user info',
                'status' : 40000
            }

        if result:
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
        name, tel = cursor.fetchall()[0]

        disconnect_database(db)

        return name, tel

    
    def deleteUser(self):
        db, cursor = connect_database()
        query = f'SELECT 1 FROM Profiles WHERE email="{self.email}"'
        cursor.execute(query)

        if len(cursor.fetchall()) == 0:
            return False

        query = f'DELETE FROM Profiles WHERE email="{self.email}"'

        cursor.execute(query)
        db.commit()

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

        return True