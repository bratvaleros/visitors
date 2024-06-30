import enum
from functools import wraps

from django.contrib.auth import get_user_model

from visit_control.permissions.permissions import EventPermissions

User = get_user_model()


class Events(enum.Enum):
    GET_DEPARTMENT = "get_department"
    GET_DEPARTMENTS = "get_departments"
    CREATE_DEPARTMENT = "create_department"
    UPDATE_DEPARTMENT = "update_department"
    DELETE_DEPARTMENT = "delete_department"
    GET_ACCOUNT = "get_account"
    GET_ACCOUNTS = "get_accounts"
    CREATE_ACCOUNT = "create_account"
    UPDATE_ACCOUNT = "update_account"


class PermissionsDenied(Exception):
    pass


def check_permissions(event_code: Events):
    def wrapper(func):

        @wraps(func)
        def check_permission(handler, *args, **kwargs):
            if args:
                raise ValueError("Pass only keyword args for permissions check")

            user = kwargs.get("user")

            if user is None:
                raise ValueError("Pass user to check permissions")

            func(handler, **kwargs)
            checker = EventPermissions(user, event_code, kwargs)
            granted: bool = checker()

            if granted is False:
                raise PermissionsDenied(checker.get_denied_message())

        return check_permission

    return wrapper
