from utils.database import ConnectSingletonDB

from model.Massa.massa import Massas


class MassaDao:
    _TABLE_NAME = 'MASSAS'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(tipo)' \
                   'values(%s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_TIPO = "SELECT * FROM {} WHERE TIPO='{}'"
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}' WHERE ID={}"

    def __init__(self):
        self.DataBase = ConnectSingletonDB().get_instance()

    def salvar(self, massa):
        if massa.id is None:
            cursor = self.DataBase.cursor()
            cursor.execute(self._INSERT_INTO, (massa.tipo))
            id = cursor.fetchone()[0]
            self.DataBase.commit()
            cursor.close()
            massa.id = id
            return massa
        else:
            raise Exception('Erro: Não é possivel salvar a tipo de massa')

    def get_all(self):
        massas = []
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_ALL)
        all_massas = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for massa_query in all_massas:
            data = dict(zip(columns_name, massa_query))
            massa = Massas(**data)
            massas.append(massa)
        cursor.close()
        return massas

    def get_by_tipo(self, tipo):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_TIPO.format(self._TABLE_NAME, tipo))
        columns_name = [desc[0] for desc in cursor.description]
        massa = cursor.fetchone()
        if not massa:
            return None
        data = dict(zip(columns_name, tipo()))
        massa = Massas(**data)
        cursor.close()
        return massa

    def get_by_id(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        columns_name = [desc[0] for desc in cursor.description]
        massa = cursor.fetchone()
        if not massa:
            return None
        data = dict(zip(columns_name, massa))
        massa = Massas(**data)
        cursor.close()
        return massa

    def delete_Massa(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.DataBase.commit()
        cursor.close()

    def update_Massa(self, massaNew, massaOld):
        cursor = self.DataBase.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
                                           'tipo', massaNew.tipo,
                                           massaOld.id))
        self.DataBase.commit()
        cursor.close()