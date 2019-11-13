from mongo.entity import Tesoro
from mongo.entity.Usuario import User


class JuegoException(ValueError):
    pass


class Juego:

    def __init__(self, diccionario_tesoros: dict = None, creador: User = None, dimensiones: list = None,
                 juego_last: dict = None):
        if juego_last:
            self.__id = str(juego_last.get('_id'))
            self.__tesoros = juego_last.get('diccionario_tesoros')
            self.__creador = juego_last.get('creador')
            self.__participantes = juego_last.get('participantes')
            self.__acabado = juego_last.get('estado')
            self.__ganador = juego_last.get('ganador')
            self.__dimensiones = juego_last.get('dimensiones')
            self.__tesoros_restantes = juego_last.get('tesoros_restantes')
        else:
            if diccionario_tesoros is None or creador is None or dimensiones is None:
                raise JuegoException('Parametros invalidos')
            self.__id = ''
            self.__tesoros = diccionario_tesoros
            self.__creador = creador.id
            self.__participantes = []
            self.__acabado = False
            self.__ganador = None
            self.__dimensiones = dimensiones
            self.__tesoros_restantes = len(self.__tesoros.keys())

    def encontrar_tesoro(self, identificador_tesoro, latitud, longitud, imagen_tesoro, descubridor: User) -> bool:
        if self.acabado:
            raise JuegoException('Juego ya finalizado')
        if descubridor.id not in self.participantes:
            raise JuegoException('Usuario no participante en el juego.')
        tesoro = self.__tesoros.get(identificador_tesoro)
        enc = False
        if tesoro and tesoro.fin:
            if not tesoro.descubierto:
                enc = tesoro.encontrar_tesoro(latitud, longitud, descubridor.id, imagen_tesoro)
                if enc:
                    self.__tesoros_restantes -= 1
                    if self.tesoros_restantes == 0:
                        self.__acabado = True
        return enc

    def add_participante(self, user: User):
        if user.id not in self.participantes:
            self.__participantes.append(user.id)

    @property
    def tesoros_restantes(self):
        return self.__tesoros_restantes

    @property
    def acabado(self):
        return self.__acabado

    @property
    def participantes(self):
        return self.__participantes

    @property
    def tesoros(self):
        return self.__tesoros

    @property
    def ganador(self):
        return self.__ganador

    @property
    def creador(self):
        return self.__creador

    @property
    def dimensiones(self):
        return self.__dimensiones

    @property
    def id(self):
        return self.__id

    def juego_to_dict(self, id_juego: bool = False) -> dict:
        dic = {"participantes": self.participantes, "estado": self.acabado, "creador": self.creador,
               "tesoros": Tesoro.generar_tesoros(self.tesoros), "ganador": self.ganador,
               "tesoros_restantes": self.tesoros_restantes, "dimensiones": self.__dimensiones}
        if id_juego:
            dic['id'] = self.id
        return dic

    def __str__(self):
        return self.id + '('+self.creador+'): ' + (
            'Activo' if not self.acabado else 'Terminado') + ', numero de tesoros restantes: ' + str(self.tesoros_restantes)+('. Ganador: '+self.ganador if self.ganador else '')
