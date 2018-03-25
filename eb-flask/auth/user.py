from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


class User():
    """User class to handle authentication"""
    def __init__(self, id, full_name, username, password):
        self._id = id
        self.full_name = full_name
        self.username = username
        self.hash_password(password)


    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    @staticmethod
    def verify_password(password, validate):
        return pwd_context.verify(password, validate)

    def generate_auth_token(self, expiration = 600, app = None):
        s = Serializer(app, expires_in=expiration)
        return s.dumps({ 'id': self._id })

    @staticmethod
    def verify_auth_token(token, mongo, app):
        s = Serializer(app)
        print(token)
        try:
            data = s.loads(token)
            print(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token

        tempUser = mongo.db.Users.find_one({'_id': data['_id']})
        user = User(tempUser['_id'], tempUser['full_name'], tempUser['username'], tempUser['password'])

        return user
