from utils.database import ConnectSingletonDB

from model.Pizzas.pizza import Pizzas

class PizzaDao:
    _TABLE_NAME = 'PIZZAS'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(bordas_id, massas_id)' \
                   'values(%s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}, {} WHERE ID={}"

    def __init__(self):
        self.DataBase = ConnectSingletonDB().get_instance()

    def salvar(self, pizza):
        if pizza.id is None:
            cursor = self.DataBase.cursor()
            cursor.execute(self._INSERT_INTO, (pizza.bordas_id, pizza.massas_id))
            id = cursor.fetchone()[0]
            self.DataBase.commit()
            cursor.close()
            pizza.id = id
            return pizza
        else:
            raise Exception('Erro: Não é possível salvar uma pizza com ID')

    def get_all(self):
        pizzas = []
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_ALL)
        all_pizzas = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for pizza_query in all_pizzas:
            data = dict(zip(columns_name, pizza_query))
            pizza = Pizzas(**data)
            pizzas.append(pizza)
        cursor.close()
        return pizzas

    def get_by_id(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        columns_name = [desc[0] for desc in cursor.description]
        pizza = cursor.fetchone()
        if not pizza:
            return None
        data = dict(zip(columns_name, id))
        pizza = Pizzas(**data)
        cursor.close()
        return pizza

    def delete_pizza(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.DataBase.commit()
        cursor.close()

    def update_pizza(self, pizzaNew, pizzaOld):
        cursor = self.DataBase.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
                                           'bordas_id='+str(pizzaNew.bordas_id),
                                           'massas_id='+str(pizzaNew.massas_id),
                                           pizzaOld.id))
        self.DataBase.commit()
        cursor.close()
