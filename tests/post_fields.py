

'''
Ejemplo demostrativo que muestra los campos de la entidad Post.
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
    api = API(access_token = '{you ACCESS token here}')

    # Obtenemos 1 post
    posts = api.get_proyect_posts(
        site = '7046d09b-1050-4ca1-8a88-4a49cb91ea6d',
        page_number = 1,
        page_size = 1,
        sort = 'retweets_desc')
    post = posts[0]


    # Imprimimos todos los campos del post con sus valores correspondientes
    for key, value in post.to_dict().items():
        print('{}: {}'.format(key, value))


    # Hay dos formas de acceder especificamente a un campo o varios:
    # Por ejemplo, queremos obtener el campo "provider" y "body"

    data = post.to_dict()
    provider, body = data['provider'], data['body']

    # O también...
    provider, body = post.provider, post.body