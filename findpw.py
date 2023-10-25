from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import Namespace
from flask_restx import reqparse
from initialize_database import connect_database
from initialize_database import disconnect_database
import string
import secrets
import smtplib
from email.mime.text import MIMEText
from decouple import config

Findpassword = Namespace('Findpassword')

pw_seq = string.ascii_letters + string.digits + '@#$%^&*()-+;,./'

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
                'message' : 'Email does not exist',
                'status' : 40000
            }

        new_pw = self.generateNewPassword(20)

        if not self.updatePassword(new_pw):
            return {
                'message' : 'Password update fail',
                'status' : 40001
            }

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
        try:
            cursor.execute(query)
        except:
            db.rollback()
            disconnect_database(db)
            return False

        db.commit()
        disconnect_database(db)
        return True


    def sendEmail(self, new_pw):
        EMAIL_HOST = config('EMAIL_HOST')
        EMAIL_POST = config('EMAIL_POST', cast=int)
        EMAIL_HOST_USER = config('EMAIL_HOST_USER')
        EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

        smtp = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        subject = 'subject : New Password Information'
        body = '''Hello,
It seems you've forgotten your password. We have generated a new password for you.
New Password: {}
Please be sure to change this password immediately after logging in.
Thank you,
Our Support Team
'''.format(new_pw)
        msg = subject + '\n\n' + body
        smtp.sendmail(EMAIL_HOST_USER, self.email, msg)
        smtp.quit()

