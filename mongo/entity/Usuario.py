from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, diccionario):
        self.id = diccionario.get('id')
        self.name = diccionario.get('name')
        self.avatar = diccionario.get('avatar')
        self.__admin = diccionario.get('admin')
        if not self.__admin:
            self.__admin = False
        self.access_tokens = diccionario.get('tokens')

    def user_to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "avatar": self.avatar, "admin": self.__admin,
                "tokens": self.access_tokens}

    @property
    def get_admin(self):
        return self.__admin
