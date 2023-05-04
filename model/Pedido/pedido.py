class Pedido:
    campos_validacao = ['pizza_id']

    def __init__(self, pizza_id, id=None):
        self.id = id
        self.pizza_id = pizza_id

    def get_data_dict(self):
        return {
            'id': self.id,
            'pizza_id': self.pizza_id
        }

    def __str__(self):
        return f'ID: {self.id}, Pizza ID: {self.pizza_id}'
