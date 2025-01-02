import datetime


class Teacher:
    def __init__(self, name: str, email: str, hashed_password: str, is_admin: bool = False,
                 reset_token: str = None, reset_token_expiry: datetime = None):
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.is_admin = is_admin
        self.reset_token = reset_token
        self.reset_token_expiry = reset_token_expiry

    def to_dict(self):
        """
            Convert the Teacher instance to a dictionary to be saved in MongoDB.
            """
        return {
            "name": self.name,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "is_admin": self.is_admin,
            "reset_token": self.reset_token,
            "reset_token_expiry": self.reset_token_expiry
        }
