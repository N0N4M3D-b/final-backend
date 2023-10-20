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
    @Login.doc(parser=signin_post)
    def post(self):
        # Parse request arguments
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

        name = self.isValidAccount()
        is_valid = (name != '')
        message = 'Login success' if is_valid else "Login fail"
        status = 200 if is_valid else 40000

        return {
            'name' : name,
            'message' : message,
            'status' : status
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
        
        

