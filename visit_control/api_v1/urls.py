from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

app_name = "api_v1"

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/swagger/", SpectacularSwaggerView.as_view(url_name="api_v1:schema"), name="swagger"),
    path("accounts/", include("visit_control.api_v1.accounts.urls", namespace="accounts")),
    path("departments/", include("visit_control.api_v1.departments.urls", namespace="departments")),
]
