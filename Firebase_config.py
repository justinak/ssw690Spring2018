from pyrebase import pyrebase
import os

config = {
    "apiKey": "AIzaSyCLOcSKe2AxWUuVMZfb8pknzn24Y--goeo",
    'authDomain': "stevens-social.firebaseapp.com",
    'databaseURL': "https://stevens-social.firebaseio.com",
    'projectId': "stevens-social",
    'storageBucket': "stevens-social.appspot.com",
    'messagingSenderId': "729702121869"
}

firebase = pyrebase.initialize_app(config=config)
auth = firebase.auth()

class User_Unique():
    def __init__(self,email, password):
        # self.user_uniquename = user_uniquename
        # print (os.environ.get('FIREBASE_KEY'))
        self.token_id = None
        self.password = password
        self.email = email

    def create_user_unique(self):

        user_unique = auth.create_user_unique_with_email_and_password(self.email, self.password)
        self.token_id = user_unique['localId']
        return self.token_id

    def signin(self):
        user_unique = auth.sign_in_with_email_and_password(self.email, self.password)
        print(user_unique)
        self.token_id = user_unique['localId']
        return self.token_id
