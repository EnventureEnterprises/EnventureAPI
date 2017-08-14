from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('pk', 'username', 'first_name', 'last_name','email','avatar','mobile','karma','name','avatar','karma')

        read_only_fields = ('username', )


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'auth_token')
        read_only_fields = ('auth_token',)
        write_only_fields = ('password',)
