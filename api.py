
'''
Script principal. Permite interactúar con la API de Shokesu.
'''

import endpoints
from resourcemapper import ResourceMapper
from request import request

class API:
    '''
    Este objeto permite hacer llamadas a la API de Shokesu.
    '''
    def __init__(self, access_token):
        '''
        Inicializa la instancia. Debe indicarse como parámetro, un
        access_token (JWT), que se añadirá en todas las requests a la
        API de Shokesu en una cabecera.
        '''
        self.access_token = access_token
        self.resource_mapper = ResourceMapper()


    def update_user(self, user, params):
        '''
        Actualiza la información de un usuario existente.
        :param user: Es el usuario cuya información se va a actualizar
        :param params: Es la información nueva del usuario. Es un diccionario que puede contener
        los siguientes valores:
        "region", "vat", "city", "address", "postalcode",
        "password", "country", "email", "company", "repeat_password"
        :return:
        '''
        raise Exception('Uninmplemented method')
        # TODO

    def delete_user(self, user):
        '''
        Elimina un usuario,
        :param user: Es el usuario a eliminar
        :return:
        '''
        # TODO
        raise Exception('Uninmplemented method')

    def add_terms_to_proyect(self, site, terms):
        '''
        Añade términos a un proyecto.
        :param site: Es el proyecto
        :param terms: Son los términos a añadir al proyecto.
        :return:
        '''
        self.request(endpoints.add_terms_to_proyect,
                     placeholders = {'site' : site},
                     use_access_token = True,
                     params = terms)


    def add_profile_to_proyect(self, site, profile):
        '''
        Añade un perfil a un proyecto.
        :return:
        '''
        self.request(endpoints.add_profile_to_proyect,
                     placeholders = {'site' : site},
                     use_access_token = True,
                     params = profile)
        # TODO

    def get_proyect_info(self, site):
        '''
        Obtiene información de un proyecto.
        :param site: Es el proyecto del que se quiere obtener información
        :return:
        '''
        self.request(endpoints.get_proyect_info,
                     placeholders = {'site' : site},
                     use_access_token = True)


    def get_profile_info(self, profile):
        '''
        Obtiene información de un perfil.
        :return:
        '''
        self.request(endpoints.get_profile_info,
                     placeholders = {'profile' : profile},
                     use_access_token = True)


    def get_profile_posts(self, profile, site = None):
        '''
        Obtiene los posts asociados a un perfil.
        :param profile Es el perfil cuyos posts queremos obtener
        :param site Indica si queremos obtener solo los posts del perfil que
        son contribuciones a un proyecto en conreto. Si es None devuelve todos los
        posts del perfil (Por defecto es None)
        :return:
        '''
        if not site is None:
            endpoint = endpoints.get_profile_posts_on_proyect
            placeholders = {'profile' : profile, 'site' : site}
        else:
            endpoint = endpoints.get_profile_posts
            placeholders = {'profile' : profile}

        self.request(endpoint = endpoint,
                     placeholders = placeholders,
                     use_access_token = True)


    def get_profiles(self, site, params):
        '''
        Obtiene todos los perfiles dentro de un proyecto.
        :return:
        '''
        self.request(endpoints.get_profiles,
                     placeholders = {'site' : site},
                     use_access_token = True,
                     params = params)



    def get_graphs(self, site, dashboard):
        '''
        Obtiene gráficos de un dashboard de un proyecto.
        :return:
        '''
        # TODO
        raise Exception('Uninplemented method')

    def get_reports(self, site, report):
        '''
        Obtener información de un informe de un proyecto en concreto.
        :param
        :return:
        '''
        # TODO
        raise Exception('Uninplemented method')


    def get_insights(self):
        # TODO
        raise Exception('Uninplemented method')

    def request(self, endpoint, placeholders = {}, use_access_token = True, params = None):
        method = endpoint.method
        path = endpoint.path(**self.resource_mapper.map_resources(**placeholders))
        response = request(method = method,
                           path = path,
                           access_token = self.access_token if use_access_token else None,
                           payload = params)
        return response
