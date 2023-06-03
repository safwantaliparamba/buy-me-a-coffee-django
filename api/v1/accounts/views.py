import json

from razorpay import Client

from django.conf import settings
from django.http.request import HttpRequest

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from accounts.models import User, Order
from api.v1.general.functions import generate_serializer_errors
from api.v1.accounts.serializers import RegisterSerializer, LoginSerializer


client = Client(auth=(settings.RAZORPAY_API_KEY,settings.RAZORPAY_CLIENT_SECRET)) 


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request: HttpRequest):
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
def login(request: HttpRequest):
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


@api_view(["POST"])
def pay(request: HttpRequest):
    user_id = request.POST.get('user_id')
    amount = request.POST.get('amount')

    print(request.POST)

    if User.objects.filter(id=user_id,is_deleted=False).exists():
        user: User = User.objects.filter(id=user_id,is_deleted=False).latest("date_joined")

        payment = client.order.create({
            "amount": int(amount) * 100,
            "currency": "INR",
            "payment_capture": "1",
        })

        order: Order = Order.objects.create(
            recipient = user,
            user = request.user,
            amount = amount,
            payment_id = payment.get("id")
        )

        response_data = {
            "statusCode" : 6000,
            "data":{
                "order_id": order.payment_id,
                "name":user.name,
                "email": user.email,
            }
        }
    else:
        response_data = {
            "statusCode": 6001,
            "data":{
                "title": "Failed",
                "message": "User not found",
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def payment_verification(request: HttpRequest):
    razorpay_order_id = request.data.get("razorpay_order_id")
    razorpay_payment_id = request.data.get("razorpay_payment_id")
    razorpay_signature = request.data.get("razorpay_signature")

    if Order.objects.filter(payment_id=razorpay_order_id,is_deleted=False).exists():
        order = Order.objects.filter(payment_id=razorpay_order_id, is_deleted=False).latest("date_added")

        data = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        check = client.utility.verify_payment_signature(data)

        print(check)

        if check:
            order.is_paid = True
            order.save()
            
            response_data = {
                "statusCode": 6000,
                "data":{
                    "title":"Success",
                    "message":"payment success"
                }
            }
        else:
            response_data = {
                "statusCode": 6001,
                "data":{
                    "title":"Failed",
                    "message":"payment failed"
                }
            }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "message": "Order not found"
            }
        }

    return Response(response_data, status= status.HTTP_200_OK)

