from DataBase.connect import ConexaoBD

from model.Status.status import Status


class StatuDao:
    _TABLE_NAME = 'STATUS'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(tipo)' \
                   'values(%s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_TIPO = "SELECT * FROM {} WHERE TIPO='{}'"
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}' WHERE ID={}"

    def __init__(self):
        self.DataBase = ConexaoBD().get_instance()

    def salvar(self, statu):
        if statu.id is None:
            cursor = self.DataBase.cursor()
            cursor.execute(self._INSERT_INTO, (statu.tipo))
            id = cursor.fetchone()[0]
            self.DataBase.commit()
            cursor.close()
            statu.id = id
            return statu
        else:
            raise Exception('Erro: Não é possivel salvar o tipo de statu')

    def get_all(self):
        status = []
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_ALL)
        all_status = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for statu_query in all_status:
            data = dict(zip(columns_name, statu_query))
            statu = Status(**data)
            status.append(statu)
        cursor.close()
        return status

    def get_by_tipo(self, tipo):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_TIPO.format(self._TABLE_NAME, tipo))
        columns_name = [desc[0] for desc in cursor.description]
        statu = cursor.fetchone()
        if not statu:
            return None
        data = dict(zip(columns_name, add_pizza()))
        statu = Status(**data)
        cursor.close()
        return statu

    def get_by_id(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        columns_name = [desc[0] for desc in cursor.description]
        statu = cursor.fetchone()
        if not statu:
            return None
        data = dict(zip(columns_name, statu))
        statu = Status(**data)
        cursor.close()
        return statu

    def delete_Statu(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.DataBase.commit()
        cursor.close()

    def update_Statu(self, statuNew, statuOld):
        cursor = self.DataBase.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
                                           'tipo', statuNew.tipo,
                                           statuOld.id))
        self.DataBase.commit()
        cursor.close()