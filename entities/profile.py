

from entities.entity import Entity, RequiredField, Field, DateField

class Profile(Entity):
    '''
    Representa la entidad perfil
    '''
    def __init__(self, data):
        super().__init__(data)


    # Definición de los campos de la entidad Profile
    friends_count = RequiredField()
    listed_count = RequiredField()
    favourites_count = RequiredField()
    verified = RequiredField()
    description = RequiredField()
    photo = RequiredField()
    url = RequiredField()
    provider = RequiredField()
    followers_count = RequiredField()
    name = RequiredField()
    location = RequiredField()
    screenname = RequiredField()
    lang = RequiredField()