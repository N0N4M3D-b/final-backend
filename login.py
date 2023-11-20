from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import Namespace
from flask_restx import reqparse
from initialize_database import connect_database
from initialize_database import disconnect_database
import jwt
import time
import os

def VerifyJWT(func):
    def checkJWT(*args, **kwargs):
        try:
            token = request.headers.get('Authorization').replace('"','').replace("'",'')
            decode = jwt.decode(token, os.environ['SECRET'], algorithms=['HS256'])
            
            if time.time() > decode['expire_time']:
                return {'message' : 'JWT Token expired', 'status' : 401}

            result = func(*args, **kwargs)
            result['token'] = jwt.encode({'email' : GetEmailFromJWT(), 'expire_time': time.time()+(60*1)}, os.environ['SECRET'], algorithm='HS256')
            
            return result
        
        except:
            return {'message' : 'JWT Token verify error', 'status' : 403}
        
    return checkJWT

def GetEmailFromJWT():
    token = request.headers.get('Authorization').replace('"','').replace("'",'')
    decode = jwt.decode(token, os.environ['SECRET'], algorithms=['HS256'])

    return decode['email']

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
            token = jwt.encode({'email' : self.email, 'expire_time': time.time()+(60*1)}, os.environ['SECRET'], algorithm='HS256')
            print(token)
            print(type(token))
            return {
                'name' : name,
                'token' : token,
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
        
        

