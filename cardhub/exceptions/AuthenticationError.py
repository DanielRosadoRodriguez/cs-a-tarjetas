

class AuthenticationError(Exception):
    '''
    Exception raised when the authentication fails
    '''
    def __init__(self):
        '''
        Constructor of the class.
        It inits the class with an established message.
        '''
        message = "Authentication failed"
        super().__init__(message)
