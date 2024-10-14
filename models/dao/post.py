import sys
import os


# Para poder ubicar la ruta del archivo a importar
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from db.cursor_pool import CursordelPool
from models.post import Post
from logs.logger import log


class PostDAO:
    """
    DAO - Data access Object para la tabla de posts
    CRUD
    """

    _SELECCIONAR = 'Select * From "posts" order by id'
    # _INSERTAR = 'INSERT INTO "posts" (username, password) values (%s,%s)'
    # _ACTUALIZAR = 'UPDATE "posts" set username=%s, password=%s Where id_user=%s'
    # _ELIMINAR = 'DELETE FROM "posts" WHERE id = %s'

    @classmethod
    def seleccionar(cls):
        # with Conexion.obtenerConexion()as conexion:
        with CursordelPool() as cursor:
            log.debug("Seleccionamos post")
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            posts = []
            for registro in registros:
                post = Post(
                    registro[0],
                    registro[1],
                    registro[2],
                    registro[3],
                    registro[4],
                )
                posts.append(post)
        return posts






if __name__ == "__main__":
    # Select
    posts = PostDAO.seleccionar()
    for post in posts:
        log.debug(post)
