from django.urls import path

from .views import AuthViewSet, LoggedInOpsViewSet


login = AuthViewSet.as_view({"post": "login"})

register = AuthViewSet.as_view({"post": "register"})

validate_token = AuthViewSet.as_view({"post": "validate_token"})

profile = LoggedInOpsViewSet.as_view({"get": "profile"})


urlpatterns = [
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("validate-token/", validate_token, name="validate_token"),
    path("profile/", profile, name="profile"),
]
