from flask import Flask
from flask_restx import Api
from flask_restx import Resource
from login import Login
from findpw import Findpassword
from register import Register
from userinfo import Userinfo
from monitoring import Monitoring
from initialize_database import InitializeDatabase

app = Flask(__name__)
api = Api(app)

api.add_namespace(Login, '/signin')
api.add_namespace(Findpassword, '/findpw')
api.add_namespace(Register, '/signup')
api.add_namespace(Userinfo, '/myinfo')
api.add_namespace(Monitoring, '/list')

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, Worajdold!'}

if __name__ == '__main__':
    InitializeDatabase()
    app.run(host='0.0.0.0', port='8080', debug=True)