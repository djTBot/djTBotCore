from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
# ----------------------------


class Ping(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        content = {'message': 'Pong: djTBotCore'}
        return Response(content)
