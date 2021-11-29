from typing import Generic
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from .serializers import LoginSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib import auth
import jwt
# Create your views here.


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            serializer.save(password=make_password(password))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        email = data.get('email', '')
        password = data.get('password', '')
        print(password)
        user = auth.authenticate(email=email, password=password)
        if user:
            print(user)
            auth_token = jwt.encode(
                {'email': user.email}, settings.JWT_SECRET_KEY, algorithm="HS256")
            serializer = UserSerializer(user)
            data = {
                'user': serializer.data, 'access': auth_token
            }
            # send response if sucessful
            return Response(data, status=status.HTTP_200_OK)

            # send response if fail
        return Response({'details': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
