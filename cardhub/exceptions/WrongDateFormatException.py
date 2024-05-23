class WrongDateFormatException(Exception):
    '''
    Exception raised when the date format is incorrect
    '''
    def __init__(self, message):
        '''
        Constructor of the class.
        It receives a message in constructor and inits the class with it.
        '''
        super().__init__(message)
    