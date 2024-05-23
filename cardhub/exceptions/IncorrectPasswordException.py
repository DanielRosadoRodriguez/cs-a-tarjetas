
class IncorrectPasswordException(Exception):
    '''
    Exception raised when the password is incorrect
    '''
    def __init__(self):
        '''
        Constructor of the class.
        It inits the class with an established message.
        '''
        incorrect_password_message = "Password is incorrect"
        super().__init__(incorrect_password_message)
        