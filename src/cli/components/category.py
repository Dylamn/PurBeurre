class Category:

    def __init__(self, data: dict):
        self.name = data.get('name')

    def __repr__(self):
        return f'<Category {self.name}/>'
