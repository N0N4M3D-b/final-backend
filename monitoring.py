from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import Namespace
from initialize_database import connect_database
from initialize_database import disconnect_database

Monitoring = Namespace('Monitoring')

@Monitoring.route('/unsolved/<int:index>')
class UnsolvedGet(Resource):
    def get(self, index):
        pass

@Monitoring.route('/solved/<int:index>')
class SolvedGet(Resource):
    def get(self, index):
        pass

@Monitoring.route('/unsolved')
class UnSolved(Resource):
    def post(self):
        try:
            self.latitude = request.json.get('latitude')
            self.longitude = request.json.get('longitude')
            self.pic = request.json.get('pic')
        except:
            print('[!] /unsolved (POST) : Invalid request data')
            return {
                'message' : 'Invalid request data',
                'status' : 400
            }
        
        try:
            self.UnsolvedInsertDatabase()
        except:
            return {
                'message' : 'Database error',
                'status' : 400
            }
        return {
            'message' : 'Register unsolved case success',
            'status' : 200
        }
        
    def UnsolvedInsertDatabase(self):
        db, cursor = connect_database()

        query = f'INSERT INTO UnsolvedCase VALUES (NULL, "{self.latitude}", "{self.longitude}", "{self.pic}", CURRENT_TIMESTAMP)'
        cursor.execute(query)
        db.commit()

    def put(self):
        pass

@Monitoring.route('/solved')
class Solved(Resource):
    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass