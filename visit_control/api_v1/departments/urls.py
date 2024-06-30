from django.urls import path, include

from visit_control.api_v1.departments.views import DepartmentsView, DepartmentView, AddDepartmentView

app_name = "clients"

urlpatterns = [
    path("", DepartmentsView.as_view()),
    path("create/", AddDepartmentView.as_view()),
    path("<int:client_id>/", DepartmentView.as_view()),
]
