class Category(object):
    """Class which represents a category

    Attributes:
        _id (int): The primary key (identifier) of the category.
        _name (str): The name of the category.
        _tag (str): The tag of the category.
        _created_at (str): The datetime when the category has been created.
        _updated_at (str): The datetime of the last update of the category.
    """

    def get_key(self):
        """Return the primary key of the entity/model"""
        return self.__getattribute__('_id')

    @property
    def name(self):
        """Get the name of the category."""
        return self.__getattribute__('_name')

    @property
    def tag(self):
        """Get the tag of the category."""
        return self.__getattribute__('_tag')

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(f'_{key}', value)

    def to_string(self):
        """Return a short string representation of the category."""
        return self.__str__()

    def __repr__(self):
        return f"<Category {self.get_key()}/>"

    def __str__(self):
        """The string representation of a category."""
        return f'Name: {self.name} | Tag: {self.tag} \n'
