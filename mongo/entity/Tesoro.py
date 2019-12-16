from datetime import datetime

from mongo.entity.Usuario import User


class Tesoro:

    def __init__(self, identificador: int = None, latitud: float = None, longitud: float = None, pista_texto=None,
                 pista_imagen=None, diccionario_mongo=None):
        if not diccionario_mongo:
            self.__identificador = identificador
            self.__latitud = latitud
            self.__longitud = longitud
            self.__descubridores = {}
            self.__pista_texto = pista_texto
            self.__pista_imagen = pista_imagen
        else:
            self.__identificador = diccionario_mongo.get('identificador')
            self.__latitud = diccionario_mongo.get('latitud')
            self.__longitud = diccionario_mongo.get('longitud')
            self.__descubridores = diccionario_mongo.get('descubridores')
            self.__pista_texto = diccionario_mongo.get('pista_texto')
            self.__pista_imagen = diccionario_mongo.get('pista_imagen')

    def cambiar_pista_texto(self, nueva_pista):
        self.__pista_texto = nueva_pista

    def cambiar_pista_imagen(self, nueva_pista):
        self.__pista_imagen = nueva_pista

    def encontrar_tesoro(self, usuario: User, latitud, longitud, imagen_tesoro) -> bool:
        latitud = float(latitud)
        longitud = float(longitud)
        if abs(latitud - self.latitud) <= 0.001 and abs(longitud - self.longitud) <= 0.001 and usuario.id_mongo not in self.descubridores:
            self.__descubridores[usuario.id_mongo] = {
                "email": usuario.id,
                "imagen_tesoro": imagen_tesoro,
                "fecha_encontrado": datetime.now().strftime("%Y-%m%d %H:%M:%S")
            }
            return True
        else:
            return False

    def reset(self):
        self.__descubridores = {}

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
    def descubridores(self) -> dict:
        return self.__descubridores

    def get_pistas(self) -> list:
        return [self.__pista_texto, self.__pista_imagen]

    def get_dict_from_tesoro(self) -> dict:
        return {"identificador": self.identificador, "latitud": self.latitud, "longitud": self.longitud,
                "descubridores": self.descubridores,
                "pista_texto": self.__pista_texto, "pista_imagen": self.__pista_imagen}


def generar_tesoros(tesoros: dict) -> dict:
    tesoros_generados = {}
    for x in tesoros.values():
        tesoros_generados[str(x.identificador)] = x.get_dict_from_tesoro()
    return tesoros_generados


def generar_tesoros_object(tesoros: dict) -> dict:
    diccionario = {}
    for t in tesoros:
        diccionario[t] = Tesoro(diccionario_mongo=tesoros.get(t))
    return diccionario
