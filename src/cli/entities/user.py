class User:
    """

    Attributes:
        id (int): The key identifier of the user.
        username (str): The username of the user.
        email (str): The email of the user.
        created_at (str): The datetime when the user sign up.
        updated_at (str): The datetime of the last update of the user.
    """

    @property
    def id(self):
        return self.__getattribute__('_id')

    @property
    def username(self):
        return self.__getattribute__('_username')
    @property
    def email(self):
        return self.__getattribute__('_email')
    @property
    def created_at(self):
        return self.__getattribute__('_created_at')
    @property
    def updated_at(self):
        return self.__getattribute__('_updated_at')

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(f'_{key}', value)


    def __repr__(self):
        return f"<User {self.id}/>"
