
class EmailNotRegisteredException(Exception):
    def __init__(self, email:str):
        self.email:str = email
        super().__init__(f"Email {email} is not registered.")