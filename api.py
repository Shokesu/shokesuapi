# coding=utf-8

'''
Script principal. Permite interactúar con la API de Shokesu.
'''

import endpoints
from resourcemapper import ResourceMapper
from request import request
from entities.post import Post
from entities.proyect import Proyect
from entities.profile import Profile

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
        raise NotImplementedError()
        # TODO

    def delete_user(self, user):
        '''
        Elimina un usuario,
        :param user: Es el usuario a eliminar
        :return:
        '''
        # TODO
        raise NotImplementedError()

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
                     payload = terms)


    def add_profile_to_proyect(self, site, profile):
        '''
        Añade un perfil a un proyecto.
        :return:
        '''
        self.request(endpoints.add_profile_to_proyect,
                     placeholders = {'site' : site},
                     use_access_token = True,
                     payload = profile)
        # TODO


    def get_proyect_info(self, site):
        '''
        Obtiene información de un proyecto.
        :param site: Es el proyecto del que se quiere obtener información
        :return:
        '''
        data = self.request(endpoints.get_proyect_info,
                            placeholders = {'site' : site},
                            use_access_token = True)
        proyect = Proyect.get_from_data(data)
        return proyect


    def get_profile_info(self, profile):
        '''
        Obtiene información de un perfil.
        :return:
        '''
        data = self.request(endpoints.get_profile_info,
                            placeholders = {'profile' : profile},
                            use_access_token = True)

        profile = Profile.get_from_data(data)
        return profile


    def get_profile_posts(self, profile, site = None, page_number = 1, page_size = 10, sort = None, filter = None):
        '''
        Obtiene los posts asociados a un perfil.
        :param profile: Es el perfil cuyos posts queremos obtener
        :param site: Indica si queremos obtener solo los posts del perfil que
        son contribuciones a un proyecto en conreto. Si es None devuelve todos los
        posts del perfil (Por defecto es None)
        :param page_number: Puede usarse para páginar los posts. Indicará que página de los posts
        queremos seleccionar. Por defecto se selecciona la primera página.
        :param page_size: Indica el tamaño de la página. Se devolverán a los sumo tantos posts como
        el tamaño de la página.
        :param sort: Indica el tipo de ordenación de los posts.
        Los posibles valores son: published_at, retweets_asc, retweets_desc, likes_asc, likes_desc
        Si no se especifica o se establece a None, el resultado no se ordena (Por defecto es None)
        :param filter: Es un parámetro opcional que determina el criterio de filtrado de los posts.
        :return: Devuelve un listado de Posts extraídos.
        '''
        if not site is None:
            endpoint = endpoints.get_profile_posts_on_proyect
            placeholders = {'profile' : profile, 'site' : site}
        else:
            endpoint = endpoints.get_profile_posts
            placeholders = {'profile' : profile}

        if not filter is None and not filter.can_be_applied_to('post'):
            raise ValueError('This filter cannot be applied on posts searches')


        data = self.request(endpoint = endpoint,
                            placeholders = placeholders,
                            params = {'pageNumber' : page_number,
                                      'pageSize' : page_size,
                                      'sort' : sort},
                            use_access_token = True,
                            payload = filter)
        return Post.get_from_data(data)


    def get_proyect_posts(self, site, page_number = 1, page_size = 10, sort = None, filter = None):
        '''
        Obtiene posts de un proyecto en concreto.
        :param site: Es la ID del proyecto del que quiere obtenerse sus perfiles.
        :param page_number: Puede usarse para páginar los posts. Indicará que página de los posts
        queremos seleccionar. Por defecto se selecciona la primera página.
        :param page_size: Indica el tamaño de la página. Se devolverán a los sumo tantos posts como
        el tamaño de la página.
        :param sort: Indica el tipo de ordenación de los posts.
        Los posibles valores son: published_at, retweets_asc, retweets_desc, likes_asc, likes_desc
        Si no se especifica o se establece a None, el resultado no se ordena (Por defecto es None)
        :param filter: Es un parámetro adicional que determina el criterio de filtrado de los posts.
        :return: Devuelve un listado de Posts extraídos.
        '''
        if not filter is None and not filter.can_be_applied_to('post'):
            raise ValueError('This filter cannot be applied on posts searches')

        data = self.request(endpoint = endpoints.get_proyect_posts,
                            placeholders = {'site' : site},
                            params={'pageNumber': page_number,
                                    'pageSize': page_size,
                                    'sort': sort},
                            use_access_token = True,
                            payload = filter)

        return Post.get_from_data(data)



    def get_profiles(self, site, filter = None):
        '''
        Obtiene todos los perfiles dentro de un proyecto.
        :param: site Es la ID del proyecto
        :param: filter Es un parámetro opcional que determina el criterio de filtrado de los
        perfiles a obtener.
        :return:
        '''
        if not filter is None and not filter.can_be_applied_to('profile'):
            raise ValueError('This filter cannot be applied on profiles searches')

        data = self.request(endpoints.get_profiles,
                            placeholders = {'site' : site},
                            use_access_token = True,
                            payload = filter)
        profiles = Profile.get_from_data(data)
        return profiles


    def get_graphs(self, site, dashboard):
        '''
        Obtiene gráficos de un dashboard de un proyecto.
        :return:
        '''
        # TODO
        raise NotImplementedError()

    def get_reports(self, site, report):
        '''
        Obtener información de un informe de un proyecto en concreto.
        :param
        :return:
        '''
        # TODO
        raise NotImplementedError()


    def get_insights(self):
        # TODO
        raise NotImplementedError()



    def request(self, endpoint, placeholders = {}, params = {}, use_access_token = True, payload = None):
        method = endpoint.method
        path = endpoint.path(**self.resource_mapper.map_resources(**placeholders))
        response = request(method = method,
                           path = path,
                           params = params,
                           access_token = self.access_token if use_access_token else None,
                           payload = payload)

        self.response = response

        try:
            return response.json()
        except:
            raise Exception('Error parsing request response from {} to JSON'.format(response.url))
