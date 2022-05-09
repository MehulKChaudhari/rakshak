from rest_framework import serializers


class UserSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=254)
    name = serializers.CharField(max_length=254)
    protection_level = serializers.CharFiedl()
    last_login = serializers.DateTimeField()
