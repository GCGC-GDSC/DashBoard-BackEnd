from rest_framework import generics, status, views, response
from django.db.models import Q, Count, Max
from .serializers import *
from .models import *

class GitList(generics.ListAPIView):
    serializer_class = GitSerializer

    def get(self, request):
        send_data = {}


class GisList(generics.ListAPIView):
    serializer_class = GisSerializer

    def get(self, request):
        send_data = {}

        return response.Response({'status': 'OK', 'result': send_data})


class PharmacyList(generics.ListAPIView):
    serializer_class = PharmacySerializer

    def get(self, request):
        send_data = {}

        return response.Response({'status': 'OK', 'result': send_data})


class Gim_BBA_BCOMList(generics.ListAPIView):
    serializer_class = Gim_MBASerializer

    def get(self, request):
        send_data = {}

        return response.Response({'status': 'OK', 'result': send_data})


class Gim_MBAList(generics.ListAPIView):
    serializer_class = Gim_MBASerializer

    def get(self, request):
        send_data = {}

        return response.Response({'status': 'OK', 'result': send_data})
