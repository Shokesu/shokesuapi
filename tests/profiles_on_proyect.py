

'''
Ejemplo que demuestra el uso del método get_profiles de la API
'''

from api import API
from logger import Logger
import logging

if __name__ == '__main__':
    # La siguiente sentencia permite guardar los mensajes de depuración en un fichero log
    # externo.
    Logger().setLevel(logging.DEBUG)

    # Creamos el objeto API. Necesitamos el JWT para tener acceso.
    api = API(access_token = '{your access token here}')
    profiles = api.get_profiles(
        site = '7046d09b-1050-4ca1-8a88-4a49cb91ea6d', # Es la ID del proyecto sobre le que queremos obtener perfiles
    )

    # Mostramos info de los perfiles

    print('Number of profiles fetched: {}'.format(len(profiles)))

    # Mostramos el primer perfil
    if len(profiles) > 0:
        profile = profiles[0]
        print(profile)