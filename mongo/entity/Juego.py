from mongo.entity import Tesoro
from mongo.entity.Usuario import User


class JuegoException(ValueError):
    pass


class Juego:

    def __init__(self, diccionario_tesoros: dict = None, creador: User = None, dimensiones: list = None,
                 juego_last: dict = None):
        if juego_last:
            self.__id = str(juego_last.get('_id'))
            self.__tesoros = Tesoro.generar_tesoros_object(juego_last.get('tesoros'))
            self.__creador = juego_last.get('creador')
            self.__participantes = juego_last.get('participantes')
            self.__estado = juego_last.get('estado')
            self.__ganador = juego_last.get('ganador')
            self.__dimensiones = juego_last.get('dimensiones')
            self.__tesoros_restantes = juego_last.get('tesoros_restantes')
        else:
            if diccionario_tesoros is None or creador is None or dimensiones is None:
                raise JuegoException('Parametros invalidos')
            self.__id = ''
            self.__tesoros = diccionario_tesoros
            self.__creador = creador.id
            self.__participantes = {}
            self.__estado = True
            self.__ganador = None
            self.__dimensiones = dimensiones
            self.__tesoros_restantes = len(self.__tesoros.keys())

    def encontrar_tesoro(self, identificador_tesoro, latitud, longitud, imagen_tesoro, descubridor: User) -> bool:
        if not self.estado:
            raise JuegoException('Juego ya finalizado')
        if descubridor.id_mongo not in self.participantes:
            raise JuegoException('Usuario no participante en el juego.')
        tesoro = self.__tesoros.get(str(identificador_tesoro))
        if not tesoro:
            raise JuegoException('Tesoro no existente')
        enc = False
        if tesoro and descubridor.id_mongo not in tesoro.descubridores:
            enc = tesoro.encontrar_tesoro(descubridor, latitud, longitud, imagen_tesoro)
            if enc:
                p = self.participantes[descubridor.id_mongo]
                p['tesoros'] = p['tesoros'] + 1
                if p['tesoros'] == len(self.tesoros):
                    self.__estado = False
                    self.__ganador = descubridor.id
                if len(self.tesoros)-p['tesoros'] < self.tesoros_restantes:
                    self.__tesoros_restantes = len(self.tesoros)-p['tesoros']
        return enc

    def add_participante(self, user: User):
        if user.id not in self.participantes:
            self.__participantes[user.id_mongo] = {"email": user.id, "tesoros": 0}

    def remove_tesoro(self, id_tesoro)->bool:
        tesoro = self.__tesoros.get(id_tesoro)
        if tesoro:
            descubridores = tesoro.descubridores
            if len(descubridores.keys()) == 0:
                self.__tesoros_restantes = self.__tesoros_restantes - 1
            else:
                lista_auxiliar_participantes = []
                for user in self.__participantes:
                    dicc = self.__participantes.get(user)
                    if len(self.tesoros) - dicc.get('tesoros') == self.__tesoros_restantes:
                        lista_auxiliar_participantes.append(user)
                for user in descubridores:
                    if user not in lista_auxiliar_participantes:
                        self.__tesoros_restantes = self.__tesoros_restantes - 1
                        break
            self.__tesoros.pop(id_tesoro)
            return True
        else:
            return False


    @property
    def tesoros_restantes(self):
        return self.__tesoros_restantes

    @property
    def estado(self):
        return self.__estado

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
        dic = {"participantes": self.participantes, "estado": self.estado, "creador": self.creador,
               "tesoros": Tesoro.generar_tesoros(self.tesoros), "ganador": self.ganador,
               "tesoros_restantes": self.tesoros_restantes, "dimensiones": self.__dimensiones}
        if id_juego:
            dic['id'] = self.id
        return dic

    def __str__(self):
        return self.id + '('+self.creador+'): ' + (
            'Activo' if self.estado else 'Terminado') + ', numero de tesoros restantes: ' + str(self.tesoros_restantes)+('. Ganador: '+self.ganador if self.ganador else '')
