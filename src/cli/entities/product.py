from src.utils import pluck


class Product(object):
    """Class which represents a product

    Attributes:
        _id (int): The key identifier of the product.
        _name (str): The name of the product.
        _generic_name (str): A generic name which represent the product.
        _brands (str): The brands of the product.
        _stores (str): A string containing the different stores where the product can be available.
        _updated_at (str): The datetime when the product has been created.
        _updated_at (str): The datetime of the last update of the product.
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
    def nutriscore(self):
        """Return the nutriscore of the product"""
        return self.__getattribute__('_nutriscore_grade')

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
        """Return the full details of the product."""
        categories_name = ', '.join(pluck(self.categories, 'name'))

        return f'Name: {self.name} | Nutriscore: {self.nutriscore}\n' \
               f'Generic name: {self.generic_name}\n\n' \
               f'Brands: {self.brands}\n\n' \
               f'Stores: {self.brands}\n\n' \
               f'Categories:\n{categories_name}\n\n' \
               f'URL Open Food Facts:\n{self._url}\n'

    def to_string(self):
        """Return a short string representation of the product."""
        return self.__str__()

    def __repr__(self):
        return f"<Product {self.get_key()}/>"

    def __str__(self):
        return f'{self.name} | Nutriscore {self.nutriscore.upper()} \n' \
               f'Stores: {self.stores} | Brands: {self.brands} \n' \
               f'OpenFoodFacts URL: \n{self._url}'
