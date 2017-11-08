
'''
Este script se encarga de convertir nombres de algunos recursos en IDs.
Por ejemplo, para convertir nombres de perfiles de usuario, nombres de proyectos o sitios a
identificadores que deben indicarse en las requests a la API de Shokesu para hacer peticiones.
'''

class ResourceMapper:
    def __init__(self):
        pass


    def map_site(self, site):
        '''
        Convierte un nombre de un proyecto en un ID que puede ser usado para identificarlo y
        referenciarlo en los parámetros de las requests.
        :param site: Es el nombre de un proyecto
        :return: Devuelve su ID
        '''
        return site


    def map_profile(self, profile):
        '''

        :param profile:
        :return:
        '''
        return profile


    def map_user(self, user):
        '''

        :param user:
        :return:
        '''
        return user


    def map_dashboard(self, dashboard):
        '''

        :param dashboard:
        :return:
        '''
        return dashboard

    def map_report(self, report):
        '''

        :param report:
        :return:
        '''
        return report


    def map_resources(self, **kwargs):
        '''
        Este método toma como parámetro un número indefinido de argumentos clave, pares
        clave = valor. Se interpreta las claves como nombres de recursos, es decir uno de los
        siguientes: 'profile', 'user', 'site', 'report', 'dashboard'
        El valor indicará el nombre del recurso. Se mapearán a sus correspondientes IDs.
        e.g:
        ids = map_resources(profile = 'myprofile', site = 'mysite')
        ids['profile'] = ID of "myprofile"
        ids['site'] = ID of "mysite"

        :param kwargs:
        :return: Devuelve en forma de diccionario las IDs de los recursos
        '''

        mapper = {
            'site' : self.map_site,
            'profile' : self.map_profile,
            'user' : self.map_user,
            'report' : self.map_report,
            'dashboard' : self.map_dashboard
        }

        try:
            return dict([(key, mapper[key](value)) for key, value in kwargs.items()])
        except:
            raise Exception('Failed mapping resources to IDs: {}'.format(kwargs))
