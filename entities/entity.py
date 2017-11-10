

'''
Este script define la clase base para definir entidades (devueltas en las requests de la API de
shokesu, como la entidad Post, Profile, ...)
También se proveen utilidades para procesar la información de estas entidades y como extraer los
datos a partir de las respuestas a las requests HTTP realizadas.
'''

from datetime import datetime
from re import match
import json

class Field:
    '''
    Define un atributo de una entidad.
    '''
    def __init__(self, selector = None, processor = None, mandatory = False, default = None):
        '''
        Inicializa la instancia.
        :param selector: Es un selector que se usará para extraer el valor de campo de los datos
        obtenidos de la request. Puede usarse por ejemplo "foo.bar" para acceder al elemento "bar"
        dentro del diccionario "foo" (Como si fuese un selector CSS)
        :param processor: Es un objeto invocable que se usa para procesar el dato extraído. Si
        es None, el dato asociado a este campo no se procesa
        :param mandatory: Indica si este campo es obligatorio o no. Por defecto es False.
        :param default: Indica un valor por defecto para el campo (solo se usa si mandatory es False)
        '''
        self.processor = processor
        self.mandatory = mandatory
        self.default = default
        self.selector = selector

    def is_mandatory(self):
        return self.mandatory

    def get_processor(self):
        return self.processor

    def get_default(self):
        return self.default

    def get_selector(self):
        return self.selector

    def __str__(self):
        if self.is_mandatory():
            return 'Required field, selector = "{}"'.format(self.get_selector())
        return 'Field, selector = "{}", default = "{}"'.format(self.get_selector(), self.get_default())

    def __repr__(self):
        return '\'{}\''.format(str(self))

class RequiredField(Field):
    '''
    Representa un campo de una entidad que es obligatorio.
    '''
    def __init__(self, selector = None, processor = None):
        super().__init__(selector, processor, mandatory = True)


class DateField(Field):
    '''
    Representa un campo de una entidad que es una fecha.
    '''
    def __init__(self, selector = None, mandatory = False, default = None):
        super().__init__(selector, self.process_date, mandatory, default)

    @staticmethod
    def process_date(date):
        result = match('^(\d{4})\-(\d{1,2})\-(\d{1,2})T(\d{1,2})\:(\d{1,2})\+.*$', date)
        if not result:
            raise Exception()
        timestamp = datetime(*[int(strnum) for strnum in result.groups()])
        return timestamp

class DataSelector:
    def __init__(self, selector):
        self.selector = selector

    def __call__(self, data):
        keys = self.selector.split('.')
        value = data

        for key in keys:
            try:
                value = value[key]
            except:
                raise KeyError('Value at {} doesnt exist'.format(self.selector))
        return value




class Entity:
    '''
    Es la clase base para definir entidades.
    '''
    def __init__(self, data):
        '''
        Instancia una entidad.
        :param data: Son los datos de la entidad en forma de diccionario, que deben ser procesados.

        '''
        fields = self.get_fields()
        for name, field in fields:
            try:
                selector = DataSelector(field.get_selector()) if not field.get_selector() is None else \
                    DataSelector(name)
                processor = field.get_processor()
                mandatory = field.is_mandatory()
                default_value = field.get_default()

                try:
                    value = selector(data)
                except Exception as exc:
                    if not mandatory:
                        value = default_value
                        processor = None
                    else:
                        raise exc

                if not processor is None:
                    try:
                        value = processor(value)
                    except Exception as exc:
                        raise Exception('Attribute value processing failed ({})'.format(str(exc)))


                self.__dict__[name] = value

            except Exception as exc:
                raise ValueError('Error loading entity "{}" attribute: {}'.format(name, str(exc)))

    @classmethod
    def get_fields(cls):
        return [(name, value) for name, value in cls.__dict__.items() if isinstance(value, Field)]


    @classmethod
    def get_from_data(cls, data):
        '''
        Este método construye las entidades extrayendo los valores de sus campos a partir de los
        datos que se pasan como parámetro (Estos datos normalmente son el resultados de una request
        a la API HTTP de Shokesu)
        :param data: Los datos de las entidades. Si es una lista, se procesará cada elemento de la misma.
        Por cada elemento, se intentará crear una entidad (con la información que este contiene), y se devolverá
        una lista con las entidades obtenidas. (Si no se pudo extraer una entidad a partir de una entrada de esta
        lista, no se generará una excepción)
        En caso contrario, debe ser un diccionario con los datos de una sola entidad. Se devolverá la entidad
        extraída (se devolverá None en caso de error al extraer la entidad  a partir de los datos)
        '''

        if isinstance(data, list):
            entities = []
            for entry in data:
                entity = cls.get_from_data(entry)
                if not entity is None:
                    entities.append(entity)
            return entities

        try:
            entity = cls(data)
            return entity
        except:
            return None


    def to_dict(self):
        '''
        :return: Devuelve un diccionario con los valores de los campos de esta entidad.
        '''
        return self.__dict__

    def to_json(self):
        '''
        Codifica los campos de esta entidad en formato JSON.
        :return:
        '''
        return json.dumps(self.to_dict())