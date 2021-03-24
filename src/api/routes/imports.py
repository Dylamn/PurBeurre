import requests
from flask import Blueprint
from src.config import Config
from src.api.models import Product
from src.api.models import Category

imports = Blueprint('imports', __name__, url_prefix='/imports')


@imports.route('/products_with_categories', methods=['POST'])
def import_products_and_categories():
    from math import ceil

    page = 1
    count = {
        'new_products': 0,
        'new_categories': 0,
    }

    # Select fields that each object will contain.
    fields = [
        # Product fields
        'product_name', 'generic_name', 'nutriscore_grade', 'brands',
        'stores', 'url',
        # Category fields
        'categories', 'categories_tags',
    ]

    params = {
        'json': True, 'action': 'process', 'page_size': 1000, 'page': page,
        'fields': ','.join(fields), 'tagtype_0': 'states', 'tag_contains_0': 'contains',
        'tag_0': 'fr:checked',
    }

    response = get_products(params)

    if not response.ok:
        return {
                   'message': 'An error occurred when connecting to the Open Food Facts API. Please try again later.'
               }, 500

    payload = response.json()

    # Calculate the last page number...
    last_page = ceil(int(payload.get('count')) / params['page_size'])

    # Save products for the first page...
    added = save_products_and_categories(payload.get('products'))

    count = update_counts(count, count_to_add=added)

    # We'll use a while loop for fetching all products.
    # We can't pull all products in a single request
    # because the maximum page size is 1000.
    while page < last_page:
        # Increment the requested page number...
        page += 1
        params['page'] = page

        response = get_products(params)

        # Stop if the response status code is not 200.
        if not response.ok:
            return {
               'message': 'An error occurred when connecting to the Open Food Facts API. '
                          'Please try again later.'
            }, 500

        payload = response.json()
        # Save each products to the DB if they doesn't already exists...
        added = save_products_and_categories(payload.get('products'))

        count = update_counts(count, count_to_add=added)

    # Log the numbers of products/categories added.
    print(count)

    return {'message': 'Import was a sucess.', 'count': count}, 200


def get_products(params):
    """Send a request to the Open Food Facts API on the search endpoint."""
    return requests.get(
        f'{Config.OPENFOODFACTS_BASE}/cgi/search.pl', params=params
    )


def save_products_and_categories(json):
    categories_added = 0
    products_added = 0

    for product in json:
        if not product.get('nutriscore_grade'):
            continue

        categories = product.get('categories').split(',')
        categories_tags = product.get('categories_tags')

        # Create the product
        saved_product = Product.first_or_create(
            search={
                'name': product.get('product_name').strip()
            },
            generic_name=product.get('generic_name'),
            brands=product.get('brands'),
            stores=product.get('stores'),
            nutriscore_grade=product.get('nutriscore_grade'),
            url=product.get('url').strip(),
        )

        if saved_product.is_recently_created:
            products_added += 1

        for name, tag in zip(categories, categories_tags):
            # Check if the category exists...
            # TODO: Refactor this part when all models inherite from BaseModel
            category = Category.query.filter_by(tag=tag).first()

            # Create the category if it doesn't exists...
            if category is None:
                category = Category.create(name=name.strip(), tag=tag)
                categories_added += 1

            saved_product.categories.append(category)

    return {
        'new_products_count': products_added,
        'new_categories_count': categories_added
    }


def update_counts(count, count_to_add):
    """Sum the products added."""
    count['new_products'] += count_to_add['new_products_count']
    count['new_categories'] += count_to_add['new_categories_count']

    return count
