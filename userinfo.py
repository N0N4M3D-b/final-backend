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

        name, tel = self.getUserInfo()

        return {
            'name' : name,
            'tel' : tel,
            'message' : 'success',
            'status' : 200
        }
        

    def delete(self):
        pass


    def put(self):
        pass

    
    def getUserInfo(self):
        db, cursor = connect_database()
        query = f'SELECT name, tel FROM Profiles WHERE email="{self.email}"'

        cursor.execute(query)
        name, tel = cursor.fetchall()[0]

        disconnect_database(db)

        return name, tel