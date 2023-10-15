from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import Namespace

Login = Namespace('Login')

@Login.route('')
class Signin(Resource):
    def post(self):
        pass