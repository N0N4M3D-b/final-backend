from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import Namespace
import string
import secrets

Findpassword = Namespace('Findpassword')

pw_seq = string.ascii_letters + string.digits + string.punctuation

@Findpassword.route('')
class Findpw(Resource):
    def post(self):
        # Parse request arguments
        try:
            self.email = request.json.get('email')
        except:
            print('[!] /findpw (POST) : Invalid request data')
            return {
                'message' : 'Invalid request data',
                'status' : 400
            }

        return {
            'new pass' : self.generateNewPassword(20)
        }


    def generateNewPassword(self, pw_length):
        new_password = ''.join([secrets.choice(pw_seq) for _ in range(pw_length)])
        return new_password
