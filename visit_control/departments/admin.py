from django.contrib import admin
from visit_control.departments.models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent")
    list_filter = ("name", "parent")
