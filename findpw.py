from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import Namespace

Findpassword = Namespace('Findpassword')

@Findpassword.route('')
class Findpw(Resource):
    def post(self):
        pass