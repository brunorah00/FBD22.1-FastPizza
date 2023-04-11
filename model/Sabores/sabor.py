class Sabores:

    campos_validacao = ['name']

    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def get_data_dict(self):
        return {
            'id': self.id,
            'Name': self.Name
        }

    def __str__(self):
        return f'Name:{self.name}'