# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time


# import psycopg2 as db
import sys
import os
from  psycopg2 import pool

# Para poder ubicar la ruta del archivo a importar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from logs.logger import log 

class Conexion:
    _DATABASE = "fastapi"
    _USERNAME = "postgres"
    _PASSWORD = "123456"
    _DB_PORT = "5432"
    _HOST = "localhost"
    _MIN_CON = 2
    _MAX_CON = 5
    _pool = None
    # _conexion = None
    # _cursor = None

    #Para obtener una Pool de conexiones..!
    @classmethod
    def obtenerPool(cls):
        if cls._pool is None:
            try:
                cls._pool = pool.SimpleConnectionPool(
                    cls._MIN_CON,
                    cls._MAX_CON,
                    host=cls._HOST,
                    port=cls._DB_PORT,
                    user=cls._USERNAME,
                    password=cls._PASSWORD,
                    database=cls._DATABASE,
                )
                log.debug(f'Conexion exitosa: {cls._pool}')
                print(f"Conexion exitosa: {cls._pool}!!")
                return cls._pool
            except Exception as e:
                print(f"Ocurrio un error al obtener el pool de conexiones")
                sys.exit()
        else:
            return cls._pool

    @classmethod
    def obtenerConexion(cls):
        #Obtener un solo objeto de conexion a la base de datos!
        conexion = cls.obtenerPool().getconn()
        log.debug(f'Conexion exitosa al obtener un pool de conexion: {conexion}')
        return conexion
 
    
    #Liberar conexion
    @classmethod
    def liberarConexion(cls, conexion):
        cls.obtenerPool().putconn(conexion)
        log.debug(f'Regresamos la conexion al pool de conexiones {conexion}!!')
    
    #Cerrar por completo la conexion
    @classmethod
    def cerrarConexion(cls):
        cls.obtenerPool().closeall()
            


# testing
if __name__ == "__main__":
    pool1 = Conexion.obtenerConexion()
    Conexion.liberarConexion(pool1)
    pool2 = Conexion.obtenerConexion()
    
    



# def conexiondb():
#     while True:
#         try:
#             conn = psycopg2.connect(
#                 host="localhost",
#                 database="fastapi",
#                 user="postgres",
#                 password="123456",
#                 cursor_factory=RealDictCursor,
#             )
#             cursor = conn.cursor()
#             print(f"Database connection was successfull {cursor}!!")
#             break
#         except Exception as error:
#             print('Connecting to database failed')
#             print(f"An exception occurred {error}")
#             time.sleep(2)
