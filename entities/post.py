# coding=utf-8
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
    published_at = DateField(mandatory = True)
    url = RequiredField()
    provider = RequiredField()
    name = RequiredField(selector = 'user.name')
    body = RequiredField(processor = lambda X:next(iter(X.values())))

    lang = RequiredField()
    kind = RequiredField()
    tipo = RequiredField(selector = 'type')

    pictures = RequiredField()
    videos = RequiredField()
    #concepts = RequiredField()
    #entities = RequiredField()
    #original_tags = RequiredField()

    favorite_count = RequiredField()
    reach_count = RequiredField()

    # Campos para posts de twitter
    is_retweet = Field()
    retweet_count = Field()
    is_reply = Field()
