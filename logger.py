# coding=utf-8


import logging
from os.path import join, dirname


class Logger:
    '''
    Esta clase se usa para enviar mensajes de depuración de la librería a un fichero
    de log externo.
    '''
    class __Singleton:
        def __init__(self):
            log_path = join(dirname(__file__), 'logs', 'shokesu_api.log')
            self.log = logging.Logger(__name__)
            self.log.addHandler(logging.FileHandler(log_path))

        def __getattr__(self, item):
            return getattr(self.log, item)

    instance = None
    def __init__(self):
        if Logger.instance is None:
            Logger.instance = Logger.__Singleton()

    def __getattr__(self, item):
        return getattr(Logger.instance, item)