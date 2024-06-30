from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from visit_control.departments.models import Department

User = get_user_model()


class EventPermissions:
    """
    Класс для проверки права выполнения конкретного действия пользователем и доступа к объектам.
    """

    def __init__(self, user, event_code, data):
        """
        :param user: Объект пользователя, для которого проверяются права.
        :param event_code: Событие, право на совершение которого необходимо проверить.
        :param data: Dict[str, Any] Данные события.

        """
        self.user = user
        self.event_code = event_code.value
        self.event_data = data

        self._denied_message: str = _("User has no permissions to do this")
        self.__pass_attrs = ["user"]  # event checker can add some attrs to pass attr_checking

    def pass_it(self, attr: str) -> None:
        """
        Добавляет переданный атрибут в список атрибутов, которые не нужно проверять. Необходимо при проверке некоторых
        событий, содержащих атрибуты не поддающиеся стандартной проверке.
        :param attr: Название атрибута, который необходимо пропустить при проверке прав.

        """
        self.__pass_attrs.append(attr)

    def _add_denied_message(self, message: str):
        """
        Метод для добавления причины отказа. Если проверка прав провалилась и есть сообщение - оно отправится
        пользователю вместо стандартного.

        """
        assert isinstance(message, str)
        self._denied_message = message

    def get_denied_message(self):
        """ Метод получения текста причины при отказе """
        return self._denied_message

    def __call__(self, *args, **kwargs):
        """
        Основной метод проверки.
        Сначала проверяет возможность выполнения события, путем поиска метода с названием "event_`self.event_code`".
        Если такой метод найден - он вызывается и проверяет возможность выполнения действия основываясь на данные
        события.
        Если метод проверки события не найден или вернул None - перебирает все атрибуты, переданные в словаре `data`,
        ищет метод "attr_`attr_name`". Если такой метод найден - он будет вызван и внутри необходимо определить, есть ли
        у текущего пользователя права на объект.

        Проверка останавливается, если метод проверки права на событие вернул `bool` или были проверены все атрибуты.
        Проверка прав на атрибуты запускается только если метод проверки прав на событие вернул `None`. Если любой из
        методов проверки прав на атрибут вернул `False` - сразу выходим с отказом.

        :return: bool

        """
        # Check event firstly.
        event_check_method_name = f"event_{self.event_code}"
        event_check_method = getattr(self, event_check_method_name, None)

        if event_check_method is not None:
            """ Если есть метод проверки события """
            event_granted = event_check_method()

            if event_granted is not None:
                """ Только если он вернул True или False - завершаем проверки """
                return event_granted

        """ Если метод проверки события не найден либо он не знает, можно ли (вернул `None`) """
        for attr_name in self.event_data:
            """ Если название атрибута в `self.__pass_attrs` - его не нужно проверять """
            if attr_name in self.__pass_attrs:
                continue

            attr_check_method_name = f"attr_{attr_name}"
            attr_check_method = getattr(self, attr_check_method_name, None)

            if attr_check_method is not None:
                """ Если есть метод проверки доступа к атрибуту """
                attr_granted = attr_check_method()

                if attr_granted is False:
                    """ Нельзя реагировать на `True`, т.к. доступ к остальным атрибутам не будет проверен """
                    return attr_granted

        # In other case
        return True

    def event_create_department(self):
        """ Суперпользователь может создать запись """
        if not self._is_superuser():
            return False
        return True

    @staticmethod
    def event_get_departments():
        """
        Получить список записей имеет право любой пользователь.
        Содержимое списка - задача не класса проверки прав.

        """
        return True

    def event_get_department(self):
        """ Получить можно только свою запись """
        if not self._is_superuser():
            return False
        return True

    def event_update_department(self):
        """ Обновить можно только свою запись """
        if not self._is_superuser():
            return False
        return True

    def event_delete_department(self):
        """ Удалить можно только свою запись """
        if not self._is_superuser():
            return False
        return True

    def _is_superuser(self, *args, **kwargs):
        return self.user.is_superuser

    @staticmethod
    def event_get_accounts():
        """
        Получить список пользователей имеет право любой пользователь.
        """
        return True

    def event_create_account(self):
        """ Суперпользователь может создать запись """
        if not self._is_superuser():
            return False
        return True

    def event_update_account(self):
        """ Суперпользователь может изменить запись """
        if not self._is_superuser():
            return False
        return True

    @staticmethod
    def event_get_account():
        """
        Получить список пользователей имеет право любой пользователь.
        """
        return True
