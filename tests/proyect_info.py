
'''
Este es un ejemplo que muestra como usar el método get_proyect_info de la API
'''


from api import API
from logger import Logger
import logging

if __name__ == '__main__':
    # La siguiente sentencia permite guardar los mensajes de depuración en un fichero log
    # externo.
    Logger().setLevel(logging.DEBUG)

    # Creamos el objeto API. Necesitamos el JWT para tener acceso.
    api = API(access_token = '{your access token HERE}')

    proyect_info = api.get_proyect_info(
        site = '7046d09b-1050-4ca1-8a88-4a49cb91ea6d', # Es la ID del proyecto sobre le que queremos obtener info.
    )

    # Imprimimos la información del proyecto.
    print(proyect_info.to_dict())