
class EmailNotRegisteredException(Exception):
    '''
    Exception raised when the email is not registered
    '''
    def __init__(self, email:str):
        '''
        Constructor of the class.
        It inits the class with a template for an error message
        that indicates that a given email was not found.
        '''
        self.email:str = email
        super().__init__(f"Email {email} is not registered.")