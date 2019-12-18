from mongo.entity.Mensaje import Mensaje
from mongo.mongo_manager import mensajes


def save_mensaje(mensaje: Mensaje):
    mensajes.insert_one(mensaje.mensaje_to_dict())


def find_all_mensajes_by_juego(id_juego: str):
    diccionario_busqueda = {'juego': id_juego}
    mensajes.find(diccionario_busqueda)


def __generar_lista_juegos(res: dict) -> list:
    lista_mensajes = []
    for x in res:
        lista_mensajes.append(__generar_mensaje(x))
    return lista_mensajes


def __generar_mensaje(res):
    return Mensaje(mensaje_dict=res)
