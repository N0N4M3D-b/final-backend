from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import Namespace

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
        pass

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