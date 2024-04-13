from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ..models import User
from cardhub.dao.UserDao import UserDao

class Authenticator:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.dao_users = UserDao()
        


    def authenticate_user(self) -> bool:
        try:
            user = self.dao_users.get(email=self.email)
            is_correct_password = user.password == self.password 
            return is_correct_password
        except User.DoesNotExist:
            print("User does not exist") 
            return False