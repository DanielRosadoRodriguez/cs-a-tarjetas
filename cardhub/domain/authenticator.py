
from cardhub.exceptions.EmailNotRegisteredException import EmailNotRegisteredException
from cardhub.exceptions.IncorrectPasswordException import IncorrectPasswordException
from cardhub.models import User

class Authenticator:
    def __init__(self, 
                 users:list[User],
                 email:str,
                 password:str):

        self._users:list[User] = users
        self._email:str = email  
        self._password:str = password

    def authenticate_user(self):
        try:
            found_user = User.objects.get(_email=self._email)
            if found_user.get_password() == self._password:
                return found_user
            else:
                raise IncorrectPasswordException()
        except User.DoesNotExist:
            raise EmailNotRegisteredException(self._email)
            

    def _is_email_registered(self):
        for user in self._users:
            if user.get_email() == self._email:
                return True
        raise EmailNotRegisteredException(self._email)

    def _is_password_correct(self):
        for user in self._users:
            if user.get_email() == self._email:
                if user.get_password() == self._password:
                    return True
        raise IncorrectPasswordException()


    