from flask import Flask
from flask import request
from flask_restx import Api
from flask_restx import Resource
import pymysql

def connect_database():
    db = pymysql.connect(host='database',
        port=3306,
        user='finaluser',
        passwd='dongafinal1234!',
        db='final',
        charset='utf8'
    )
    cursor = db.cursor()

    return db, cursor

def disconnect_database(db):
    db.commit()
    db.close()

app = Flask(__name__)
api = Api(app)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, World!'}

@api.route('/data')
class Data(Resource):
    def post(self):
        print('TEST1')
        lat = request.json.get('latitude')
        lon = request.json.get('longitude')
        pic = request.json.get('pic')
        print('TESTAA')
        db, cursor = connect_database()
        print('TEST')
        query = 'INSERT INTO UnsolvedCase (latitude, longitude, image) VALUES(%s,%s,%s)'
        cursor.execute(query, (lat, lon, pic))
        print('TEST2')
        disconnect_database(db)
        print('TEST3')
        return {'message': 'Add data success', 'status': 200}

@api.route('/data/solved')
class Solved(Resource):
    def get(self):
        pass

@api.route('/data/solved/<int:id>')
class SolvedID(Resource):
    def get(self):
        pass

    def put(self):
        pass

@api.route('/data/unsolved')
class UnSolved(Resource):
    def get(self):
        pass

@api.route('/data/unsolved/<int:id>')
class UnSolvedID(Resource):
    def get(self):
        pass

    def put(self):
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)