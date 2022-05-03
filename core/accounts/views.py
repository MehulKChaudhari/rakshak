from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.forms import ValidationError
from django.db import IntegrityError
from django.contrib.auth import authenticate

from .models import User
from .serializers import UserSerializer


class AuthViewSet(ViewSet):
    def register(self, request: Request) -> Response:

        data = request.data
        email = data.get("email", None)
        password = data.get("password", None)
        name = data.get("name", None)
        message, status_code = None, None

        if email and password:

            try:
                validate_email(email)

                try:
                    validate_password(password=password)

                    try:
                        user = User.objects.create_user(
                            email=email, password=password, name=name
                        )
                        message, status_code = (
                            "User registered scuccessfully",
                            status.HTTP_201_CREATED,
                        )

                    except IntegrityError as e:
                        message, status_code = (
                            "User with this email already exists",
                            status.HTTP_400_BAD_REQUEST,
                        )

                except ValidationError as e:
                    message, status_code = (
                        e.args[0][0].message,
                        status.HTTP_400_BAD_REQUEST,
                    )

            except ValidationError as e:
                message, status_code = e.message, status.HTTP_400_BAD_REQUEST

        else:

            message, status_code = (
                "Supply fields: email, password",
                status.HTTP_400_BAD_REQUEST,
            )

        return Response(data={"message": message}, status=status_code)

    def login(self, request: Request) -> Response:

        data = request.data
        email = data.get("email", None)
        password = data.get("password", None)
        message, status_code = None, None

        if not any((email, password)):

            message, status_code = (
                "Supply fields: email, password",
                status.HTTP_400_BAD_REQUEST,
            )

        else:

            user = authenticate(request, username=email, password=password)

            if user:

                token = Token.objects.get(user=user)
                serialized_user = UserSerializer(user)
                message, status_code = {
                    "token": token.key,
                    "profile": serialized_user.data,
                }, status.HTTP_200_OK

            else:

                message, status_code = "Wrong credentails", status.HTTP_400_BAD_REQUEST

        return Response(data={"message": message}, status=status_code)

    def forgot_password(self, request: Request) -> Response:
        pass

    def validate_token(self, request: Request) -> Response:
        data = request.data
        token = data.get("token")
        if Token.objects.filter(key=token).exists():
            return Response({}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class LoggedInOpsViewSet(ViewSet):

    persmission_classes = (IsAuthenticated,)

    def profile(self, request: Request) -> Response:
        message, status_code = None, None
        serialized_user = UserSerializer(request.user)
        message, status_code = serialized_user.data, status.HTTP_200_OK
        return Response({"message": message}, status=status_code)

    def update_user_info(self, request: Request) -> Response:
        pass
