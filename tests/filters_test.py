
'''
Ejemplo que muestra como buscar posts de un proyecto usando filtros.
'''


from api import API
from logger import Logger
import logging
from entities.post import Post
from filters import *


if __name__ == '__main__':
    # La siguiente sentencia permite guardar los mensajes de depuración en un fichero log
    # externo.
    Logger().setLevel(logging.DEBUG)


    # Creamos el objeto API. Necesitamos el JWT para tener acceso.
    api = API(access_token = '{your access token here}')


    # Creamos filtros para refinar la búsqueda de posts
    filters = [
        # Solo posts de twitter de usuarios cuya cantidad de seguidores oscila entre 100 y 1000
        only_twitter & Followers(min = 100, max = 1000),

        # Posts de twitter y facebook de usuarios que están siguiendo a entre 0 y 300 personas.
        Provider('twitter', 'facebook') & Friends(min = 0, max = 300),

        # Posts de usuarios verificados de facebook o twitter
        Provider('twitter', 'facebook') & verified,

        # Y además, que los perfiles de los usuarios estén monotorizados...
        Provider('twitter', 'facebook') & verified & monitoring,

        # Posts que han sido marcados como favoritos entre 50-100 veces publicados por perfiles
        # verificados y etiquetados (solo twitter)
        only_twitter & verified & tagged & Applauses(min = 50, max = 100),

        # Posts de twitter o facebook, compartidos entre 100 y 200 veces.
        Provider('twitter', 'facebook') & Shared(min = 100, max = 200),

        # Filtrado por contenido. Posts con fotos de twitter de usuarios verificados...
        only_twitter & verified & only_photos,

        # Filtrado por lenguaje. Posts en español de twitter
        only_twitter & PostLang('es'),

        # Filtrado por lenguaje detectado en el perfil de los usuarios.
        # Posts de twitter publicados por usuarios verificados siendo el idioma detectado en
        # el perfil español o inglés
        only_twitter & verified & UserLang('es', 'en')
    ]

    # Selecciona el filtro que quieres utilizar
    filter = filters[8]

    # obtenemos el listado de posts filtrados
    posts = api.get_proyect_posts(
        site = '7046d09b-1050-4ca1-8a88-4a49cb91ea6d', # ID del perfil del cual queremos obtener sus posts
        page_number = 1,
        page_size = 10,
        filter = filter)

    # Imprimimos los posts
    for post in posts:
        print(post)
