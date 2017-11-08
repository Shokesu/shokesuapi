
'''
Este script define los endpoints de la API de shokesu (métodos y rutas)
e.g:
str(update_user) == 'POST /register'
update_user.method == 'POST'
update_user.path == '/register'

Los endpoints pueden tener placeholders...
add_terms_to_proyect.path == 'POST /site/$1/terms'
add_terms_to_proyect.placeholders == ['site']

Para rellenar los placeholders...

add_terms_to_proyect.path(site = 'mysite') == '/site/mysite/terms'

También se añade documentación sobre la API de shokesu.
'''


class PathWrapper:
    def __init__(self, path, placeholders=[]):
        self.path = path
        self.placeholders = placeholders

    def __call__(self, **kwargs):
        path = self.path
        for i in range(0, len(self.placeholders)):
            placeholder = self.placeholders[i]
            try:
                path = path.replace('${}'.format(i+1), kwargs[placeholder])
            except:
                raise ValueError('No value for "{}" placeholder on "{}" endpoint'.format(placeholder, str(self)))
        return path

    def __str__(self):
        return self.path

class Endpoint:
    def __init__(self, method, path, placeholders = []):
        self.method = method
        self.path = PathWrapper(path, placeholders)
        self.placeholders = placeholders

    def __str__(self):
        return '{} {}'.format(self.method, self.path)



register_user = Endpoint(
    method = 'POST',
    path = '/register',
    placeholders = []
)

update_user = Endpoint(
    method = 'PUT',
    path = '/user/$1',
    placeholders = ['user']
)

delete_user = Endpoint(
    method = 'DELETE',
    path = '/user/$1',
    placeholders = ['user']
)

add_terms_to_proyect = Endpoint(
    method = 'POST',
    path = '/site/$1/terms',
    placeholders = ['site']
)

add_profile_to_proyect = Endpoint(
    method = 'POST',
    path = '/site/$1/getprofiles',
    placeholders = ['site']
)

get_proyect_info = Endpoint(
    method = 'GET',
    path = '/site/$1',
    placeholders = ['site']
)

get_profile_info = Endpoint(
    method = 'GET',
    path = '/profile/$1',
    placeholders = ['profile']
)

get_profile_posts = Endpoint(
    method = 'POST',
    path = '/profile/$1/posts',
    placeholders = ['profile']
)

get_profile_posts_on_proyect = Endpoint(
    method = 'POST',
    path = '/profile/$1/site/$2/posts',
    placeholders = ['profile', 'site']
)

get_profiles = Endpoint(
    method = 'POST',
    path = '/site/$1/getprofiles',
    placeholders = ['site']
)

get_graphs = Endpoint(
    method = 'POST',
    path = '/site/$1/dashboard/$2',
    placeholders = ['site', 'dashboard']
)

get_reports = Endpoint(
    method = 'GET',
    path = '/site/$1/report/$2',
    placeholders = ['site', 'report']
)

get_insights = Endpoint(
    method = 'POST',
    path = '/profile/$1/pdfReport',
    placeholders = ['profile']
)