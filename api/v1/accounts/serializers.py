import json
import requests

from django.http.request import HttpRequest

from rest_framework import serializers

from accounts.models import User
from general.encryptions import encrypt, decrypt


def authenticate(request: HttpRequest, email: str, password: str):
    user: User = User.objects.filter(email=email).latest("date_joined")

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "email": email,
        "password": password,
    }

    protocol = "http://"

    if request.is_secure():
        protocol = "https://"

    host = request.get_host()
    url = protocol + host + "/api/v1/accounts/token/"

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:

        return {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "email": user.email,
                "name": user.name,
                "refresh": response.json().get("refresh"),
                "access": response.json().get("access"),
            }
        }
    
    return {
        "statusCode": 6001,
        "data": {
            "title": "Failed",
            "message": "Token generation failed"
        }
    }



class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=128)
    password = serializers.CharField(min_length=6, max_length=128)


    def validate(self, attrs):
        email = attrs.get('email')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Email already exists"})
        
        return super().validate(attrs)
    
    def save(self, **kwargs):
        request = kwargs.get("request")

        name = self._validated_data.get("name")
        email = self._validated_data.get("email")
        password = self._validated_data.get("password")

        user: User = User.objects.create_user(
            name=name, 
            email=email,
            password=password,
            encrypted_password=encrypt(password)
        )

        return authenticate(request,email,password)
        
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, max_length=128)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not User.objects.filter(email=email, is_deleted=False).exists():
            raise serializers.ValidationError({"email":"User not found"})
        
        user:User = User.objects.filter(email=email).latest("date_joined")

        if password != decrypt(user.encrypted_password):
            raise serializers.ValidationError({"password":"Incorrect password"})
        
        return super().validate(attrs)
    
    def save(self, **kwargs):
        request = kwargs.get("request")

        email = self._validated_data.get("email")
        password = self._validated_data.get("password")
        
        return authenticate(request, email, password)