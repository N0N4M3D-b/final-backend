from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import Namespace

Userinfo = Namespace('Userinfo')

@Userinfo.route('')
class Myinfo(Resource):
    def post(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass