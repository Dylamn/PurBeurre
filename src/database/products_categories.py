from src.api import db

# Create a `products_categories` table representation.
products_categories = db.Table(
    'products_categories',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)
