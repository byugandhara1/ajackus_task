from django.contrib.auth import get_user_model,password_validation
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager

from .models import Content

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff','auth_token')
        read_only_fields = ('id', 'is_active', 'is_staff')

    def get_auth_token(self, obj):
        token = Token.objects.filter(user=obj)
        if token:

            token = token[0]
        else:
            token = Token.objects.create(user=obj)
        return token.key


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the user
    """

    class Meta:
        model = User
        fields = ('email', 'password', 'username','fullname','mobile',' address','city','state','country',' pincode','is_author')


    def validate_email(self, value):
        import email
        user = User.objects.filter(email=email)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value



class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['title', 'body', 'summary', 'category']


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model=Content
        fields=['title','body','summary','category']



