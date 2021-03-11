class Product(object):
    """Class which represents a product

    Attributes:
        _id (int): The key identifier of the user.
        _name (str): The username of the user.
        _generic_name (str): The email of the user.
        _brands (str): The brands of the product.
        _stores (str): A string containing the different stores where the product can be available.
        _updated_at (str): The datetime of the last update of the user.
    """

    def get_key(self):
        """Return the primary key of the entity/model"""
        return self.__getattribute__('_id')

    @property
    def name(self):
        """Get the name of the product."""
        return self.__getattribute__('_name')

    @property
    def generic_name(self):
        """Get the generic name of the product."""
        value = self.__getattribute__('_generic_name')

        return value if value else 'N/A'

    @property
    def stores(self):
        """Get the stores where the product can be found."""
        value = self.__getattribute__('_stores')

        return value if value else 'N/A'

    @property
    def brands(self):
        """Get the brands of the product."""
        value = self.__getattribute__('_brands')

        return value if value else 'N/A'

    @property
    def categories(self):
        """Get the categories of the product."""
        return self.__getattribute__('_categories')

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(f'_{key}', value)

    def get_details(self):
        return f'Name: {self.name}' \
               f'Generic name: {self.generic_name}' \
               f'Brands: {self.brands}'

    def to_string(self):
        """Return a string representation of the product."""
        return self.__str__()

    def __repr__(self):
        return f"<Product {self.get_key()}/>"

    def __str__(self):
        return f'{self._name}' \
               f' | Nutriscore {self._nutriscore_grade.upper()} \n' \
               f'Stores: {self.stores} | Brands: {self.brands} \n' \
               f'OpenFoodFacts URL: {self._url}'
