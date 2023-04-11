from DataBase.connect import ConexaoBD

from FastPizza.model.Sabores.sabor import Sabores


class SaborDao:
    _TABLE_NAME = 'SABORES'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(name)' \
                   'values(%s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_NAME = "SELECT * FROM {} WHERE NAME='{}'"
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}' WHERE ID={}"

    def __init__(self):
        self.DataBase = ConexaoBD().get_instance()

    def salvar(self, sabor):
        if sabor.id is None:
            cursor = self.DataBase.cursor()
            cursor.execute(self._INSERT_INTO, (sabor.name))
            id = cursor.fetchone()[0]
            self.DataBase.commit()
            cursor.close()
            sabor.id = id
            return sabor
        else:
            raise Exception('Erro: Não é possivel salvar o tipo de sabor')

    def get_all(self):
        sabores = []
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_ALL)
        all_sabores = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for sabor_query in all_sabores:
            data = dict(zip(columns_name, sabor_query))
            sabor = sabores(**data)
            sabores.append(sabor)
        cursor.close()
        return sabores

    def get_by_name(self, name):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_NAME.format(self._TABLE_NAME, name))
        columns_name = [desc[0] for desc in cursor.description]
        sabor = cursor.fetchone()
        if not sabor:
            return None
        data = dict(zip(columns_name, add_pizza()))
        sabor = Sabores(**data)
        cursor.close()
        return sabor

    def get_by_id(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        columns_name = [desc[0] for desc in cursor.description]
        sabor = cursor.fetchone()
        if not sabor:
            return None
        data = dict(zip(columns_name, sabor))
        sabor = Sabores(**data)
        cursor.close()
        return sabor

    def delete_Sabor(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.DataBase.commit()
        cursor.close()

    def update_Sabor(self, saborNew, saborOld):
        cursor = self.DataBase.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
                                           'name', saborNew.name,
                                           saborOld.id))
        self.DataBase.commit()
        cursor.close()