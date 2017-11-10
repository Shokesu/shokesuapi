
from entities.entity import Entity, Field, RequiredField, DateField


class Proyect(Entity):
    '''
    Esta entidad representa un proyecto o "site"
    '''
    def __init__(self, data):
        super().__init__(data)


    # Definición de los campos de la entidad proyecto
    id = RequiredField(),
    created_at = DateField(selector = 'created', mandatory = True)
    last_update_at = DateField(selector = 'updated', mandatory = True)
    created_by = RequiredField(selector = 'createdby')
    last_update_by = RequiredField(selector = 'updatedby')
    is_active = RequiredField(selector = 'isactive')
    description = RequiredField()
    title = RequiredField()
