from razorpay import Client

from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

# from accounts.models import User
from api.v1.general.functions import generate_serializer_errors
from api.v1.accounts.serializers import RegisterSerializer, LoginSerializer


client = Client(auth=(settings.RAZORPAY_API_KEY,settings.RAZORPAY_CLIENT_SECRET)) 


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serialized = RegisterSerializer(data=request.data)

    if serialized.is_valid():
        response_data = serialized.save(request=request)
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title": "Validation error",
                "message": generate_serializer_errors(serialized._errors)
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serialized = LoginSerializer(data=request.data)

    if serialized.is_valid():
        response_data = serialized.save(request=request)
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title": "Validation error",
                "message": generate_serializer_errors(serialized._errors)
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)