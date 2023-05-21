from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, Worajdold!'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)