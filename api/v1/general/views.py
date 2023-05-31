from django.http.request import HttpRequest

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status


@api_view(["GET"])
@permission_classes([AllowAny])
def test(request: HttpRequest):
    return Response("test",status=status.HTTP_200_OK)