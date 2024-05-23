
from cardhub.exceptions.EmailNotRegisteredException import EmailNotRegisteredException
from cardhub.exceptions.IncorrectPasswordException import IncorrectPasswordException
from cardhub.models import User

class Authenticator:
    '''
    Class that authenticates a user.
    '''
    def __init__(self, 
                 users:list[User],
                 email:str,
                 password:str):

        self._users:list[User] = users
        self._email:str = email  
        self._password:str = password

    def authenticate_user(self):
        '''
        IN: self, users, email, password
        OUT: User
        It authenticates a user by checking if the email is registered'''
        try:
            # We try to get an user with the given email, if it is not found, we raise an exception
            found_user = User.objects.get(_email=self._email)
            # Look if the password is the same as the one the given email has
            if found_user.get_password() == self._password:
                return found_user
            else:
                raise IncorrectPasswordException()
        except User.DoesNotExist:
            raise EmailNotRegisteredException(self._email)
            

    def _is_email_registered(self):
        '''
        IN: self
        OUT: bool
        It checks if the email is registered in the system.
        '''
        for user in self._users:
            if user.get_email() == self._email:
                return True
        raise EmailNotRegisteredException(self._email)

    def _is_password_correct(self):
        '''
        IN: self
        OUT: bool
        It checks if the password is correct.
        '''
        for user in self._users:
            if user.get_email() == self._email:
                if user.get_password() == self._password:
                    return True
        raise IncorrectPasswordException()


    