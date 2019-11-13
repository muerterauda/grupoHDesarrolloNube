from datetime import datetime


class Tesoro:

    def __init__(self, identificador: int, latitud: float, longitud: float, pista_texto=None, pista_imagen=None):
        self.__identificador = identificador
        self.__latitud = latitud
        self.__longitud = longitud
        self.__descubierto = False
        self.__descubridor = None
        self.__imagen_tesoro_encontrado = None
        self.__fecha_encontrado = None
        self.__pista_texto = pista_texto
        self.__pista_imagen = pista_imagen

    def cambiar_pista_texto(self, nueva_pista):
        self.__pista_texto = nueva_pista

    def cambiar_pista_imagen(self, nueva_pista):
        self.__pista_imagen = nueva_pista

    def encontrar_tesoro(self, latitud, longitud, usuario, imagen_tesoro) -> bool:
        if latitud == self.latitud and longitud == self.longitud:
            self.__descubierto = True
            self.__descubridor = usuario
            self.__imagen_tesoro_encontrado = imagen_tesoro
            self.__fecha_encontrado = datetime.now().strftime("%Y-%m%d %H:%M:%S")
            return True
        else:
            return False

    @property
    def identificador(self):
        return self.__identificador

    @property
    def latitud(self):
        return self.__latitud

    @property
    def longitud(self):
        return self.__longitud

    @property
    def descubierto(self):
        return self.__descubierto

    @property
    def descubridor(self):
        return self.__descubridor

    @property
    def fecha_encontrado(self):
        return self.__fecha_encontrado

    def get_pistas(self) -> list:
        return [self.__pista_texto, self.__pista_imagen]

    def get_prueba(self):
        return self.__imagen_tesoro_encontrado

    def get_dict_from_tesoro(self) -> dict:
        return {"id": self.identificador, "latitud": self.latitud, "longitud": self.longitud, "descubierto": self.descubierto,
                "descubridor": self.descubridor, "fecha_encontrado": self.fecha_encontrado,
                "pista_texto": self.__pista_texto, "pista_imagen": self.__pista_imagen,
                "imagen_tesoro_encontrado": self.__imagen_tesoro_encontrado}


def generar_tesoros(tesoros: dict) -> dict:
    tesoros_generados = {}
    for x in tesoros.values():
        tesoros_generados[str(x.identificador)] = x.get_dict_from_tesoro()
    return tesoros_generados
