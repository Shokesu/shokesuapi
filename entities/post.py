
from entities.entity import Entity, Field, RequiredField, DateField

class Post(Entity):
    '''
    Representa un post de alguna red social realizado por algun perfil monotorizado en la app
    de Shokesu
    '''
    def __init__(self, data):
        super().__init__(data)


    # Definición de los campos de la entidad Post
    id = RequiredField(selector = 'post_id')
    videos = RequiredField()
    source = RequiredField()
    body = RequiredField(processor = lambda X:next(iter(X.values())))
    pictures = RequiredField()
    url = RequiredField()
    concepts = RequiredField()
    provider = RequiredField()
    entities = RequiredField()
    original_tags = RequiredField()
    lang = RequiredField()
    kind = RequiredField()
    channel_id = RequiredField()

    favorite_count = RequiredField()
    reach_count = RequiredField()

    published_at = DateField(mandatory = True)

    # Campos para posts de twitter
    is_retweet = Field()
    retweet_count = Field()
    is_reply = Field()
