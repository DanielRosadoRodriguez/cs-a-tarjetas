
class CardNotFoundError(Exception):
    def __init__(self, card_name):
        message = f"Card with name {card_name} was not found"
        super().__init__(message)


    