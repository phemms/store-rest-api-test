import hmac

from models.user import UserModel


def authenticate(username, password):
    """
    This function gets called when a user calls the /auth endpoint
    with their username and password
    :param username: username in string format
    :param password: unencrypted password in string format
    :return: A UserModel object if authentication is successful, None otherwise
    """

    user = UserModel.find_by_username(username)
    if user and hmac.compare_digest(user.password, password):
        return user


def identity(payload):
    """
    This function gets called when a user has already been authenticated
    and Flask_extended-JWT verifies that their authorization header is correct
    :param payload: A dictionary with identity key which is the user id
    :return: A UserModel object
    """

    user_id = payload['sub']
    user = UserModel.find_by_id(user_id)
    #user = UserModel.query.get(user_id)
    if user:
        return user
    raise Exception(f'Error loading the user {user_id}')