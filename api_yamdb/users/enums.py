from enum import Enum


class UserRoles(Enum):
    """Класс-перечисление для выбора ролей пользователей"""
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'

    @classmethod
    def choices(cls):
        """Определяет соответствие ролей и их значений."""
        return tuple((attribute.name, attribute.value) for attribute in cls)
