from utils.database import ConnectSingletonDB

from model.Borda.borda import Bordas


class BordaDao:
    _TABLE_NAME = 'BORDAS'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(tipo)' \
                   'values(%s, %s) RETURNING id'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_TIPO = "SELECT * FROM {} WHERE TIPO='{}'"
    _SELECT_BY_ID = 'SELECT * FROM {} WHERE ID={}'
    _DELETE = 'DELETE FROM {} WHERE ID={}'
    _UPDATE = "UPDATE {} SET {}='{}', {}='{}' WHERE ID={}"

    def __init__(self):
        self.DataBase = ConnectSingletonDB().get_instance()

    def salvar(self, borda):
        if borda.id is None:
            cursor = self.DataBase.cursor()
            cursor.execute(self._INSERT_INTO, borda.tipo)
            id = cursor.fetchone()[0]
            self.DataBase.commit()
            cursor.close()
            borda.id = id
            return borda
        else:
            raise Exception('Erro: Não é possivel salvar o tipo de borda')

    def get_all(self):
        bordas = []
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_ALL)
        all_bordas = cursor.fetchall()
        columns_name = [desc[0] for desc in cursor.description]
        for borda_query in all_bordas:
            data = dict(zip(columns_name, borda_query))
            borda = Bordas(**data)
            bordas.append(borda)
        cursor.close()
        return bordas

    def get_by_tipo(self, tipo):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_TIPO.format(self._TABLE_NAME, tipo))
        columns_name = [desc[0] for desc in cursor.description]
        borda = cursor.fetchone()
        if not borda:
            return None
        data = dict(zip(columns_name, borda))
        borda = Bordas(**data)
        cursor.close()
        return borda

    def get_by_id(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
        columns_name = [desc[0] for desc in cursor.description]
        borda = cursor.fetchone()
        if not borda:
            return None
        data = dict(zip(columns_name, borda))
        borda = Bordas(**data)
        cursor.close()
        return borda

    def delete_Borda(self, id):
        cursor = self.DataBase.cursor()
        cursor.execute(self._DELETE.format(self._TABLE_NAME, id))
        self.DataBase.commit()
        cursor.close()

    def update_Borda(self, bordaNew, bordaOld):
        cursor = self.DataBase.cursor()
        cursor.execute(self._UPDATE.format(self._TABLE_NAME,
                                           'tipo', bordaNew.tipo,
                                           bordaOld.id))
        self.DataBase.commit()
        cursor.close()
