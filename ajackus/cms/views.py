from django.http import Http404
from django.shortcuts import render

from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .utils import get_and_authenticate_user, create_user_account
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView
from .models import Content
from.serializers import UserSearchSerializer,ContentSerializer
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication

User = get_user_model()

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]


    serializer_classes = {
        'login': serializers.UserLoginSerializer,
        'register': serializers.UserRegisterSerializer
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    @action(methods=['POST', ], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)




class UserSearchList(ListAPIView):
    queryset = Content.objects.all()
    serializer_class = UserSearchSerializer
    filter_backends = [SearchFilter]
    search_fields=['title','body','summary','category']

class ContentView(APIView):
    authentication_classes = [BasicAuthentication, ]
    permission_classes = [IsAuthenticated,]

    def get(self,request):

        snippet = Content.objects.filter(user_id=request.user.email)
        print('user name',request.user.email)
        serializer = ContentSerializer(snippet, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class Contentdetailview(RetrieveUpdateDestroyAPIView):
    authentication_classes = [BasicAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

