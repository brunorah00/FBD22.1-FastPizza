class Pizzas:
    campos_validacao = ['sabor', 'bordas_id', 'massas_id']

    def __init__(self, sabor, bordas_id, massas_id, id=None):
        self.id = id
        self.sabor = sabor
        self.bordas_id = bordas_id
        self.massas_id = massas_id

    def get_data_dict(self):
        return {
            'id': self.id,
            'sabor': self.sabor,
            'bordas_id': self.bordas_id,
            'massas_id': self.massas_id
        }

    def __str__(self):
        return f'Sabor: {self.sabor}, Bordas_id: {self.bordas_id}, Massas_id: {self.massas_id}'
