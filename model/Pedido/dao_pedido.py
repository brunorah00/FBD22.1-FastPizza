class PedidoDao:
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
