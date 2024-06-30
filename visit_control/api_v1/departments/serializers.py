from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from visit_control.departments.models import Department
from visit_control.utils.constants import DEPARTMENT_NAME_MAX_LENGTH


class WriteGetDepartmentSerializer(serializers.Serializer):
    pass


class WriteUpdateDepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=DEPARTMENT_NAME_MAX_LENGTH, label=_("Наименование"), required=False)


class WriteAddDepartmentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=DEPARTMENT_NAME_MAX_LENGTH, label=_("Наименование"), required=True)


class ReadDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "name", "parent")
