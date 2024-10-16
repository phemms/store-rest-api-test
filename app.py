import os

from flask import Flask, jsonify, request, g
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token

from security import authenticate, identity
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister



app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'phemms123'
api = Api(app)


jwt =JWTManager(app) # /auth


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')



@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_payload):
    #print("JWT Payload:", jwt_payload)
    g.jwt_header = jwt_header
    return identity(jwt_payload)

@app.route('/auth', methods=['POST'])
def auth_handler():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username, password)
    if user:
        access_token = create_access_token(identity=user.id)  # or user.username, depending on your needs
        return jsonify(access_token=access_token), 200
    return jsonify(message='Invalid credentials'), 401


@jwt.unauthorized_loader
def auth_error_handler(err):
    return jsonify({'message': 'Could not authorize. '
                               'Did you include a valid authorization header?'}), 401

if __name__ == '__main__':
    from db import db

    db.init_app(app)

    #if app.config['DEBUG']:
        #@app.before_first_request
        #def create_tables():
    with app.app_context():
        db.create_all()

    app.run(port=5000)
