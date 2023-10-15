from flask import request
from flask_restx import Api
from flask_restx import Resource
from flask_restx import Namespace

Register = Namespace('Register')

@Register.route('')
class Signup(Resource):
    def post(self):
        pass