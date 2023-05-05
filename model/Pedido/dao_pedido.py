class PedidoDao:

    _TABLE_NAME = 'PEDIDOS'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(pizza_id)' \
                   'values(%s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_TIPO = "SELECT * FROM {} WHERE TIPO='{}'"
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}' WHERE ID={}"


    pedidos = []
    last_id = 0

    def get_all(self):
        return self.pedidos

    def get_by_id(self, id):
        for pedido in self.pedidos:
            if pedido.id == id:
                return pedido
        return None

    def salvar(self, pedido):
        self.last_id += 1
        pedido.id = self.last_id
        self.pedidos.append(pedido)
        return pedido

    def delete_pedido(self, id):
        pedido = self.get_by_id(id)
        if pedido:
            self.pedidos.remove(pedido)

    def update_pedido(self, new_pedido, old_pedido):
        old_pedido.pizza_id = new_pedido.pizza_id
