from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import Namespace
from flask_restx import reqparse
from initialize_database import connect_database
from initialize_database import disconnect_database

Login = Namespace('Login')

@Login.route('')
class Signin(Resource):
    def post(self):
        # Parse request arguments
        try:
            self.email = request.json.get('email')
            self.password = request.json.get('password')
        except:
            print('[!] /signin (POST) : Invalid request data')
            return {
                'message' : 'Invalid request data',
                'status' : 400
            }

        name = self.isValidAccount()

        if name != '':
            return {
                'name' : name,
                'message' : 'Login success',
                'status' : 200
            }
        else:
            return {
                'message' : 'Login fail',
                'status' : 40000
            }


    # Verify if it's a valid account and return name
    def isValidAccount(self):
        db, cursor = connect_database()
        query = f'SELECT name FROM Profiles WHERE email="{self.email}" AND password="{self.password}"'
        cursor.execute(query)
        result = cursor.fetchall()

        disconnect_database(db)

        if len(result) != 0:
            return result[0][0]
        else:
            return ''
        
        

