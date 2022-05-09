from django.urls import path

from .views import AuthViewSet, LoggedInOpsViewSet


login = AuthViewSet.as_view({"post": "login"})

register = AuthViewSet.as_view({"post": "register"})

delete = AuthViewSet.as_view({"post": "delete"})

validate_token = AuthViewSet.as_view({"post": "validate_token"})

profile = LoggedInOpsViewSet.as_view({"get": "profile"})

update_protection = LoggedInOpsViewSet.as_view({"post": "update_protection"})


urlpatterns = [
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("delete/", delete, name="delete"),
    path("validate-token/", validate_token, name="validate_token"),
    path("profile/", profile, name="profile"),
    path("update-protection/", update_protection, name="update_protection"),
]
