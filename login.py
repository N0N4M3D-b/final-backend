from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import Namespace
from flask_restx import reqparse
from initialize_database import connect_database
from initialize_database import disconnect_database

Login = Namespace('Login')

signin_post = reqparse.RequestParser()
signin_post.add_argument('email', type=str, help='Please enter your email')
signin_post.add_argument('password', type=str, help='Please enter your password')

@Login.route('')
class Signin(Resource):
    @Register.doc(parser=signin_post)
    def post(self):
        # request parsing
        try:
            args = signin_post.parse_args()

            self.email = args['email']
            self.password = args['password']

        except:
            print('[!] /signin (POST) : Invalid request data')
            return {
                'message' : 'Invalid request data',
                'status' : 400
            }

        
        

