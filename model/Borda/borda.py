class Bordas:

    campos_validacao = ['tipo']

    def __init__(self, tipo, id=None):
        self.id = id
        self.tipo = tipo

    def get_data_dict(self):
        return {
            'id': self.id,
            'Tipo': self.tipo
        }

    def __str__(self):
        return f'Tipo:{self.tipo}'