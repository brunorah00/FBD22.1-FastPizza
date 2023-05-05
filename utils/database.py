import psycopg2


class ConnectSingletonDB:
    _instance = None

    def __init__(self):
        try:
            self._connect = psycopg2.connect(
                host="localhost",
                database="fastpizzas",
                user="postgres",
                password=""
            )
            print("Conexão bem sucedida!")
        except psycopg2.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def connect(self):
        return self._connect
