
class BaseFilter(dict):
    '''
    Clase base para las clases Filter y ComposedFilter.
    '''
    def __init__(self, types = None):
        super().__init__()
        self.contents = {}
        super().update({
            'filter' : self.contents
        })
        if types is None:
            types = ['post', 'dashboard', 'profile']
        self.types = types

    def can_be_applied_to(self, type):
        return type in self.types


    def __getitem__(self, key):
        return self.contents[key]

    def __setitem__(self, key, value):
        self.contents[key] = value

    def __str__(self):
        return '{}, avaliable for this search types: {}'.format(
            super().__str__(),
            ', '.join(['"{}"'.format(type) for type in self.types]))


class Filter(BaseFilter):
    '''
    Representa un filtro al hacer búsquedas en la api de shokesu
    (para refinar búsquedas de posts, perfiles o dashboards)
    '''
    name = 'unknown filter'
    types = ['post', 'dashboard', 'profile']

    def __init__(self, params):
        super().__init__(self.__class__.types)
        self[self.__class__.name] = params

    def __and__(self, other):
        '''
        Crea un filtro compuesto combinandolo con otro distinto.
        :param other: Es otro filtro para combinar con este.
        :return:
        e.g: ByContentType(video = True) & ByDate(...)
        '''
        composition = ComposedFilter()
        composition.add(self)
        return composition & other



class ComposedFilter(BaseFilter):
    '''
    Representa una combinación de filtros
    '''
    def __init__(self):
        super().__init__()


    def add(self, other):
        self.contents.update(other.contents)
        self.types = list(set(self.types) & set(other.types))


    def __and__(self, other):
        '''
        Combina este filtro compuesto con otro filtro, o con otro filtro compuesto.
        :param other: Es un filtro, o un filtro compuesto.
        :return:
        '''
        composition = ComposedFilter()
        composition.add(self)
        composition.add(other)
        return composition





####### LISTADO DE FILTROS

class Provider(Filter):
    '''
    Filtrado por red social.
    Es compatible con todo tipo de búsquedas.
    '''
    name = 'provider'
    types = ['post', 'dashboard', 'profile']

    def __init__(self, *args):
        '''
        Inicializa la instancia.
        :param *args: Se pueden especificar nombres de redes sociales. Deben ser algunas de estas:
        "twitter", "youtube", "instagram", "googleplus", "facebook", "medium", "rss"
        e.g: Provider('twitter', 'youtube')
        '''
        providers = args
        super().__init__(providers)


class FilterRange(Filter):
    '''
    Es una clase auxiliar. Es usada como clase base para filtros que seleccionan posts,
    dashboards o perfiles teniendo una propiedad en un determinado rango númerico.
    '''
    def __init__(self, min, max):
        params = {
            'from' : min,
            'to' : max
        }
        super().__init__(params)


class Followers(FilterRange):
    '''
    Filtrado por número de seguidores.
    Es compatible para búsquedas por: posts, dashboards y perfiles
    '''
    name = 'following_count'
    types = ['post', 'dashboard', 'profile']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Friends(FilterRange):
    '''
    Filtrado por número de personas a las que se está siguiendo.
    Es compatible con todo tipo de búsquedas.
    '''
    name = 'friends_count'
    types = ['post', 'dashboard', 'profile']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DailyPublishedPosts(FilterRange):
    '''
    Filtrado por número medio de posts publicados al día realizado por un perfil.
    Es compatible con todo tipo de búsquedas.
    '''
    name = 'posts_avg'
    types = ['post', 'dashboard', 'profile']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ListedCount(FilterRange):
    '''
    Filtrado por número de listas en la que está incluido un perfil.
    Solo disponible para TWITTER
    Es compatible con todo tipo de búsquedas.
    '''
    name = 'listed_count'
    types = ['post', 'dashboard', 'profile']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Verified(Filter):
    '''
    Realiza el filtrado de forma que solo se incluyen los perfiles verificados.
    Es compatible con todo tipo de búsquedas.
    '''
    name = 'verified'
    types = ['post', 'dashboard', 'profile']

    def __init__(self):
        super().__init__(True)

class Monitoring(Filter):
    '''
    Realiza un filtrado para que solo se incluyan perfiles monotorizados.
    Es compatible con todo tipo de búsquedas.
    '''
    name = 'monitoring'
    types = ['post', 'dashboard', 'profile']

    def __init__(self):
        super().__init__(True)


class Tagged(Filter):
    '''
    Es un filtro que puede usarse para incluir o descartar perfiles etiquetados dentro de
    algún proyecto.
    Es compatible con todo tipo de búsquedas
    '''
    name = 'tagged'
    types = ['post', 'dashboard', 'profile']

    def __init__(self):
        super().__init__(True)


class Sentiment(FilterRange):
    '''
    Filtra por sentimiento.
    Es compatible con posts y dashboards
    '''
    name = 'sentiment'
    types = ['post', 'dashboard']

    def __init__(self, min, max):
        '''
        Inicializa la instancia.
        :param min Debe ser el valor mínimo de sentimiento, en el rango [-100, 100]
        :param max Debe ser el valor máximo de sentimiento, en el rango [-100, 100]. Debe ser mayor
        que min.
        Un valor -100 indicaría que el sentimiento es completamente negativo. Por otro lado,
        100 sería completamente positivo. 0 es sentimiento neutro.
        '''
        super().__init__(min, max)


class Applauses(FilterRange):
    '''
    Filtro por número de "aplausos". Número de veces que una publicación o dashboard ha sido
    marcado como favorito.
    Es compatible para búsquedas de tipo "dashboard" y "post"
    '''
    name = 'favorite_count'
    types =  ['post', 'dashboard']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Shared(FilterRange):
    '''
    Realiza un filtrado por número de veces en que una publicación o dashboard ha sido compartida.
    Solo es compatible para búsquedas de tipo "dashboard" y "post"
    '''
    name = 'shared_count'
    types = ['post', 'dashboard']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Views(FilterRange):
    '''
    Filtra por la cantidad de veces que una publicación ha sido visualizada.
    Solo es compatible para búsquedas de tipo "dashboard" y "post"
    Este filtro se aplica exclusivamente para YOUTUBE
    '''
    name = 'view_count'
    types = ['post', 'dashboard']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ContentType(Filter):
    '''
    Filtrado por tipo de contenido.
    Es compatible para búsquedas de: posts y dashboards
    '''
    name = 'content_type'
    types = ['post', 'dashboard']

    def __init__(self, *args):
        '''
        Inicializa la instancia
        :param *args: Pueden especificarse los siguientes valores:
        "post", "photo", "video", "link"
        e.g: ContentType('post', 'video')
        '''
        types = args
        super().__init__(types)



class PostType(Filter):
    '''
    Filtra por tipo de publicación: original / retweet / reply
    Es compatible para búsquedas de posts y dashboards
    Exclusivo para Twitter ?
    '''
    name = 'post_type'
    types = ['post', 'dashboard']

    def __init__(self, *args):
        '''
        Inicializa la instancia.
        :param *args: Pueden especificarse los siguientes valores:
        "original", "retweet" y "reply"
        e.g: PostType('original', 'reply')
        '''
        types = args
        super().__init__(types)


class PostLang(Filter):
    '''
    Filtra por idioma de la publicación
    Es compatible para búsquedas de: "post" y "dashboard"
    '''
    name = 'lang_post'
    types = ['post', 'dashboard']

    def __init__(self, *args):
        '''
        Inicializa la instancia
        :param *args: Es un listado de identificadores de lenguajes e.g: PostLang('en', 'es')
        '''
        langs = args
        super().__init__(langs)


class UserLang(Filter):
    '''
    Filtra por idioma detectado en los perfiles
    Es compatible para todo tipo de búsquedas
    '''
    name = 'lang_user'
    types = ['post', 'dashboard', 'profile']

    def __init__(self, *args):
        langs = args
        super().__init__(langs)



class Date(Filter):
    name = 'date'
    types = ['post', 'dashboard', 'profile']
    # TODO






only_twitter = Provider('twitter')
only_youtube = Provider('youtube')
only_instagram = Provider('instagram')
only_googleplus = Provider('googleplus')
only_facebook = Provider('facebook')
only_medium = Provider('medium')
only_rss = Provider('rss')


verified = Verified()
monitoring = Monitoring()
tagged = Tagged()

only_posts = ContentType('post')
only_photos = ContentType('photo')
only_videos = ContentType('video')
only_links = ContentType('link')

only_originals = PostType('original')
only_retweets = PostType('retweet')
only_replies = PostType('reply')
