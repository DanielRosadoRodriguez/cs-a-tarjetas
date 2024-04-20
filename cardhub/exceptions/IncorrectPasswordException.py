
class IncorrectPasswordException(Exception):
    def __init__(self):
        incorrect_password_message = "Password is incorrect"
        super().__init__(incorrect_password_message)
        