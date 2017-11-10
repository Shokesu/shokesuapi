
'''
Este script es un ejemplo de como usar la API de Shokesu para obtener posts asociados a un
perfil monotorizado.
'''

from api import API
from logger import Logger
import logging
from entities.post import Post

if __name__ == '__main__':
    # La siguiente sentencia permite guardar los mensajes de depuración en un fichero log
    # externo.
    Logger().setLevel(logging.DEBUG)

    # Creamos el objeto API. Necesitamos el JWT para tener acceso.
    api = API(access_token = '{your access token here}')

    posts = api.get_profile_posts(
        profile = '46078800', # ID del perfil del cual queremos obtener sus posts
        page_number = 1,
        page_size = 5,
        sort = 'retweets_desc'
    )

    # Imprimimos los mensajes de los posts.
    for post in posts:
        print(post.body)

    # Para obtener un listado con los campos disponibles (para el primer post)...
    if len(posts) > 0:
        print(list(posts[0].to_dict().keys()))

    # Para obtener un listado de los campos de la entidad Post (y metainformación de los mismos)...
    print(Post.get_fields())
