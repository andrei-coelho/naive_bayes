import mysql.connector
from mysql.connector import Error
from util.config import Config

database = Config.instance().getDataBase()

class mysqli:
    _instance = None
    _db = None

    def __enter__(self):
        return self.instance()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __init__(self):
        try:
            self._db = mysql.connector.connect(
                host=database['host'],
                user=database['user'],
                password=database['pass'],
                database=database['dbas']
            )
            if self._db.is_connected():
                print("Conexão estabelecida com sucesso.")
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance._db

    def close(self):
        if self._db.is_connected():
            self._db.close()
            print("Conexão fechada.")