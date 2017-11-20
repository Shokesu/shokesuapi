'''
Este es un ejemplo de como usar el método get_proyect_posts de la API
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

    # obtenemos el listado de posts
    posts = api.get_proyect_posts(
        site = '7046d09b-1050-4ca1-8a88-4a49cb91ea6d', # ID del perfil del cual queremos obtener sus posts
        page_number = 1,
        page_size = 5,
        sort = 'retweets_desc')



    # Imprimimos los mensajes de los posts.
    for post in posts:
        print(post.body)
