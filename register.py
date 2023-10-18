from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import Namespace

Register = Namespace('Register')

@Register.route('')
class Signup(Resource):
    def post(self):
        try:
            email = request.json.get('email')
            name = request.json.get('name')
            password = request.json.get('password')
            tel = request.json.get('tel')
        except:
            print('[!] /signup (POST) : Invalid request data')
            return {
                'message' : 'Invalid request data',
                'status' : 400
            }
        
        