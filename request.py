

'''
Este módulo se encarga de gestionar las requests a la API de Shokesu
'''

import requests, json
from re import match, search, DOTALL
from logger import Logger
from urllib.parse import urlencode

# URI raíz de la API de Shokesu
# api_uri_root = 'https://api.shokesu.com'
api_uri_root = 'https://app.shokesu.com:8443/shokesu'


def request(method, path, params = {}, access_token = None, payload = None):
    '''
    Envia una request HTTP a la API de Shokesu.
    :param method: Es el método a utilizar. Deberá ser uno de los siguientes
    GET, PUT, POST, DELETE
    :param path Es la ruta del recurso a obtener, relativa a https://api.shokesu.com
    :param params Es un diccionario que indicará los parámetros a añadir a la URL.
    :param access_token Es un token JWT que se usará para autenticar al cliente. (Si es None,
    no se añadira a la cabecera)
    :param payload Parámetros a añadir al cuerpo de la request. Por defecto es None. Si no es
    None, deberá ser un objeto convertible a JSON. El objeto se codificará en dicho formato y
    se incluirá en el payload.
    :return:
    '''

    params = dict([(key, value) for key, value in params.items() if not value is None])

    # Construimos la url
    result = match('^\/?(.*)$', path)
    path = result.group(1)
    url = '{}/{}?{}'.format(api_uri_root, path, urlencode(params))

    send_request = {
        'GET' : requests.get,
        'POST' : requests.post,
        'PUT' : requests.put,
        'DELETE' : requests.delete
    }

    logger = Logger()

    if payload is None and method == 'POST':
        payload = {}
    payload = json.dumps(payload) if not payload is None else None
    headers = {}
    if not access_token is None:
        headers['Authorization'] = 'Bearer {}'.format(access_token)

    logger.debug('-------------\n')
    logger.debug('Sending {} request to {}'.format(method, url))
    logger.debug('Headers: ')
    logger.debug('\n'.join(['{}: {}'.format(key, value) for key, value in headers.items()]))

    response = send_request[method](url = url, data = payload, headers = headers)
    logger.debug('Response status code: {}'.format(response.status_code))

    try:
        if response.status_code == 404:
            raise Exception('404 Error Not Found')

        if response.status_code != 200:
            try:
                description =  search('<b>description<\/b>[^<]*<u>([^<]+)<\/u>', response.text, DOTALL).group(1)
            except:
                description = 'Unknown server error'
            raise Exception(description)

    except Exception as e:
        raise Exception('Error executing request to {}: {}'.format(response.url, str(e)))
    try:
        logger.debug('Response body: ')
        logger.debug(response.text)
        logger.debug('-------------\n')
        return response.json()
    except:
        raise Exception('Error parsing request response from {} to JSON'.format(response.url))