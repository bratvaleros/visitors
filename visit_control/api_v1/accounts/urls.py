from django.urls import path

from visit_control.api_v1.accounts.views import (
    ChangePasswordView,
    GetMeView,
    LoginView,
    LogoutView,
    AccountsView,
    CreateAccountView,
    AccountView,
    SetAccountPasswordView,
)

app_name = "accounts"

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("me/", GetMeView.as_view()),
    path("password/change/", ChangePasswordView.as_view()),
    path("", AccountsView.as_view()),
    path("create/", CreateAccountView.as_view()),
    path("<int:account_id>/", AccountView.as_view()),
    path("set_account_password", SetAccountPasswordView.as_view()),
]
