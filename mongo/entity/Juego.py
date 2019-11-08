from mongo.entity.Usuario import User


class JuegoException(ValueError):
    pass


class Juego:

    def __init__(self, lista_tesoros: dict, creador: User):
        self.__id = ''
        self.__tesoros = lista_tesoros
        self.__creador = creador.id
        self.__participantes = []
        self.__acabado = False
        self.__ganador = None
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
        if user.id not in self.__participantes:
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
    def id(self):
        return self.__id
