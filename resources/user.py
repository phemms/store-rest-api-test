from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    """
    This resource allows a user to register by sending a
    Post with their username and password
    """

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str,
                        required=True,
                        help='username field cannot be blank!')

    parser.add_argument('password', type=str,
                        required=True,
                        help='password field cannot be blank!')


    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exist'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User successfully created'}, 201

