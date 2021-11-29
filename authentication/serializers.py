from django.db.models import fields
from .models import User
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=4)
    first_name= serializers.CharField(max_length=255, min_length=2)
    last_name= serializers.CharField(max_length=255, min_length=2, allow_null=False, allow_blank=False)
    username= serializers.CharField(max_length=255,  allow_null=False, allow_blank=False)

    class Meta:
        model = User
        fields= ['password', 'first_name', 'last_name', 'email','username']
        
    def validate_username(self, username):
        if len(username) < 2:
            raise serializers.ValidationError({'username':('username is too short')})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username':('username already exist')})
        return super().validate(username)
    
    
    
    # def validate(self, attrs):
    #     username = attrs('username')
    #     if len(username) < 2:
    #         raise serializers.ValidationError({'username':('username is too short')})
    #     return super().validate(attrs)

    

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'email':('Email is already in use')})
        return super().validate(attrs)
    
    
    
class LoginSerializer(serializers.ModelSerializer):
        password = serializers.CharField(max_length=65, min_length=8, write_only=True)
        email = serializers.EmailField(max_length=255, min_length=4)
        
        class Meta:
            model = User
            fields = ['email', 'password']

    
    # def create(self, validated_data):
    #     return User.objects.create(**validated_data)
    
