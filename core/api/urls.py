from django.urls import path

from .views import APIViewSet


parse_string_social = APIViewSet.as_view({
    "post": "parse_string_social"
})


urlpatterns = [
    path("parse-string-social/", parse_string_social, name="parse_string_social")
]
