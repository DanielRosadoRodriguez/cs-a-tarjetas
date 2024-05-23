
class CardNotFoundError(Exception):
    '''
    Exception raised when the card is not found
    '''
    def __init__(self, card_name):
        '''
        Constructor of the class.
        It inits the class with a template for an error message 
        that indicates that a given card was not found.
        '''
        message = f"Card with name {card_name} was not found"
        super().__init__(message)


    