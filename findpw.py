from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import Namespace
import string
import secrets
import smtplib
from email.mime.text import MIMEText

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

        if not self.isValidEmail():
            return {
                'message' : 'Email does not exist'
                'status' : 40000
            }

        new_pw = self.generateNewPassword(20)
        self.updatePassword(new_pw)
        self.sendEmail(new_pw)

        return {
            'message' : 'Success',
            'status' : 200
        }



    # Verify if it's a valid email
    def isValidEmail(self):
        db, cursor = connect_database()
        query = f'SELECT 1 FROM Profiles WHERE email="{self.email}"'
        cursor.execute(query)
        result = cursor.fetchall()

        disconnect_database(db)

        return len(result) != 0


    def generateNewPassword(self, pw_length):
        new_pw = ''.join([secrets.choice(pw_seq) for _ in range(pw_length)])
        return new_pw


    def updatePassword(self, new_pw):
        db, cursor = connect_database()
        query = f'UPDATE Profiles SET password="{new_pw}" WHERE email="{self.email}"'
        cursor.execute(query)
        disconnect_database(db)


    def sendEmail(self, new_pw):

