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
        lat = request.json.get('latitude')
        lon = request.json.get('longitude')
        pic = request.json.get('pic')

        db, cursor = connect_database()
        query = 'INSERT INTO UnsolvedCase (latitude, longitude, image) VALUES(%s,%s,%s)'
        cursor.execute(query, (lat, lon, pic))
        db.commit()

        disconnect_database(db)

        return {'message': 'Add data success', 'status': 200}

@api.route('/data/solved')
class Solved(Resource):
    def get(self):
        db, cursor = connect_database()
        query = 'SELECt * FROM SolvedCase'
        cursor.execute(query)
        result = cursor.fetchall()
        disconnect_database(db)

        ret = {"datas" : []}
        tmp_data = {}

        for data in result:
            tmp_data["data_id"] = data[0]
            tmp_data["latitude"] = data[1]
            tmp_data["longitude"] = data[2]
            tmp_data["pic"] = data[3]

            ret["datas"].append(tmp_data)

        ret["message"] = "Get solved datas success"
        ret["status"] = 200

        return ret

@api.route('/data/solved/<int:caseNum>')
class SolvedID(Resource):
    def get(self, caseNum):
        db, cursor = connect_database()
        query = f'SELECT * FROM SolvedCase WHERE caseNum={caseNum}'
        cursor.execute(query)
        result = cursor.fetchall()
        data = result[0]
        disconnect_database()

        tmp_data = {}
        tmp_data["caseNum"] = data[0]
        tmp_data["latitude"] = data[1]
        tmp_data["longitude"] = data[2]
        tmp_data["pic"] = data[3]

        ret = {"data" : tmp_data}

        ret["message"] = "Get solved data success"
        ret["status"] = 200

        return ret

    def put(self, caseNum):
        db, cursor = connect_database()
        query = f'SELECT * FROM SolvedCase WHERE caseNum={caseNum}'
        cursor.execute(query)
        result = cursor.fetchall()
        data = result[0]
        
        query = 'INSERT INTO UnsolvedCase (latitude, longitude, image) VALUES(%s,%s,%s)'
        cursor.execute(query, (data[1], data[2], data[3]))
        db.commit()

        query = f'DELETE FROM SolvedCase WHERE caseNum={data[0]}'
        cursor.execute(query)
        db.commit()

        disconnect_database(db)

        ret = {}
        ret["message"] = "SolvedCase changed to UnsolvedCase"
        ret["status"] = 200

        return ret

@api.route('/data/unsolved')
class UnSolved(Resource):
    def get(self):
        db, cursor = connect_database()
        query = 'SELECt * FROM UnsolvedCase'
        cursor.execute(query)
        result = cursor.fetchall()
        disconnect_database(db)

        ret = {"datas" : []}
        tmp_data = {}

        for data in result:
            tmp_data["caseNum"] = data[0]
            tmp_data["latitude"] = data[1]
            tmp_data["longitude"] = data[2]
            tmp_data["pic"] = data[3]

            ret["datas"].append(tmp_data)


        ret["message"] = "Get unsolved datas success"
        ret["status"] = 200

        return ret

@api.route('/data/unsolved/<int:caseNum>')
class SolvedID(Resource):
    def get(self, caseNum):
        db, cursor = connect_database()
        query = f'SELECT * FROM UnsolvedCase WHERE caseNum={caseNum}'
        cursor.execute(query)
        result = cursor.fetchall()
        data = result[0]
        disconnect_database(db)

        tmp_data = {}
        tmp_data["caseNum"] = data[0]
        tmp_data["latitude"] = data[1]
        tmp_data["longitude"] = data[2]
        tmp_data["pic"] = data[3]

        ret = {"data" : tmp_data}

        ret["message"] = "Get solved data success"
        ret["status"] = 200

        return ret

    def put(self, caseNum):
        db, cursor = connect_database()
        query = f'SELECT * FROM UnsolvedCase WHERE caseNum={caseNum}'
        cursor.execute(query)
        result = cursor.fetchall()
        data = result[0]
        
        query = 'INSERT INTO SolvedCase (latitude, longitude, image) VALUES(%s,%s,%s)'
        cursor.execute(query, (data[1], data[2], data[3]))
        db.commit()

        query = f'DELETE FROM UnsolvedCase WHERE caseNum={data[0]}'
        cursor.execute(query)
        db.commit()

        disconnect_database(db)

        ret = {}
        ret["message"] = "UnsolvedCase changed to SolvedCase"
        ret["status"] = 200

        return ret

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
