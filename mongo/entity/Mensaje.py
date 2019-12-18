import datetime

from mongo.entity.Juego import Juego
from mongo.entity.Usuario import User


class MensajeException(ValueError):
    pass

class Mensaje:

    def __init__(self, user:User=None, juego:str=None, mensaje:str=None, mensaje_dict:dict=None):
        if mensaje_dict:
            self.__id = mensaje_dict['_id']
            self.__creador = mensaje_dict['creador']
            self.__mensaje = mensaje_dict['mensaje']
            self.__fecha = mensaje_dict['fecha']
            self.__juego = mensaje_dict['juego']
        else:
            if not user or not juego or not mensaje:
                raise MensajeException('Parametros de creacion incorrectos')
            self.__creador = user.id
            self.__mensaje = mensaje
            self.__fecha = str(datetime.datetime.now())
            self.__juego = juego
            self.__id = None

    @property
    def creador(self):
        return self.__creador

    @property
    def mensaje(self):
        return self.__mensaje

    @property
    def fecha(self):
        return self.__fecha

    @property
    def juego(self):
        return self.__juego

    @property
    def id(self):
        return self.__id

    def mensaje_to_dict(self, id_mensaje: bool = False) -> dict:
        dic = {'creador': self.creador, 'juego': self.juego, 'fecha': self.fecha, 'mensaje': self.mensaje}
        if id_mensaje:
            dic['id'] = self.id
        return dic
