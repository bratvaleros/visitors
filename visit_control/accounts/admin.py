from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from visit_control.accounts.models import Account


@admin.register(Account)
class AccountAdmin(DjangoUserAdmin):
    list_display = ('id', 'username', 'group', 'first_name', 'email', 'is_superuser', 'is_active', 'last_login')
    list_filter = ('username', 'is_superuser', 'is_active')
    fieldsets = (
        ('Авторизация', {'fields': ('last_login', 'username', 'password')}),
        ('Имя пользователя', {'fields': ('first_name',)}),
        ('Адрес почты', {'fields': ('email',)}),
        ('Настройки доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ';'.join(groups)
    group.short_description = 'Роли'
