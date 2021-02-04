class User:
    """

    Attributes:
        id (int): The key identifier of the user.
        username (str): The username of the user.
        email (str): The email of the user.
        created_at (str): The datetime when the user sign up.
        updated_at (str): The datetime of the last update of the user.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)


    def __repr__(self):
        return f"<User {self.id}/>"
