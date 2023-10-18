from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import Namespace
from flask_restx import reqparse
from initialize_database import connect_database
from initialize_database import disconnect_database

Register = Namespace('Register')

signup_post = reqparse.RequestParser()
signup_post.add_argument('email', type=str, help='email')
signup_post.add_argument('name', type=str, help='name')
signup_post.add_argument('password', type=str, help='password')
signup_post.add_argument('tel', type=str, help='tel')

@Register.route('')
class Signup(Resource):
    @Register.doc(parser=signup_post)
    def post(self):
        try:
            args = signup_post.parse_args()

            self.email = args['email']
            self.name = args['name']
            self.password = args['password']
            self.tel = args['tel']
        except:
            print('[!] /signup (POST) : Invalid request data')
            return {
                'message' : 'Invalid request data',
                'status' : 400
            }
        
        # Check email WhiteList
        # todo -> status 40000

        # handle email exist in Profiles exception
        if not self.checkIsExist():
            return {
                'message' : 'Already exist email',
                'status' : 40001
            }
    
        self.insertDatabase()

        return {
            'message' : 'Signup success',
            'status' : 200
        }

    def checkIsExist(self):
        exist_flag = True

        db, cursor = connect_database()

        query = f'SELECT email FROM Profiles WHERE email = "{self.email}"'
        cursor.execute(query)
        if len(cursor.fetchall()) != 0:
            print('[!] /signup (POST) : Exist email')
            exist_flag = False

        disconnect_database(db)

        return exist_flag
    
    def insertDatabase(self):
        db, cursor = connect_database()

        query = f'INSERT INTO Profiles VALUES ("{self.email}", "{self.name}", "{self.password}", "{self.tel}")'
        cursor.execute(query)
        db.commit()