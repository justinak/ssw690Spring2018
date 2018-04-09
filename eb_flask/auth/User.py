from passlib.apps import custom_app_context as pwd_context


class User():
    """User class to handle authentication"""

    def __init__(self, id, full_name, username, password):
        self._id = id
        self.full_name = full_name
        self.username = username
        self.hash_password(password)

    def is_authenticated(self):
        """Checks if the user is authenticated in"""
        return True

    def is_active(self):
        """check if the user is active"""
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        """returns the id"""
        return chr(self._id).encode('UTF-32')

    def get_password(self):
        """return Hash password"""
        return self.password

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    @staticmethod
    def verify_password(password, validate):
        return pwd_context.verify(password, validate)
