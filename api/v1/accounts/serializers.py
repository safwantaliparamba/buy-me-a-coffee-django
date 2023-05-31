from rest_framework import serializers

from accounts.models import User
from general.encryptions import encrypt, decrypt
from general.functions import authenticate


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