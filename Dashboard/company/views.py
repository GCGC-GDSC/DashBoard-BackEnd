from rest_framework import generics, status, views, response
from django.db.models import Q, Count, Max
from .serializers import *
from .models import *

class GitUgList(generics.ListAPIView):
    serializer_class = GitUgSerializer

    def get(self, request, institute):
        print("institute", institute)
        send_data = {'GIT': "this should work!!"}
        git = Git_ug.objects.all()
        print("----------------------------------------------")
        print(git)
        print("----------------------------------------------")

        return response.Response({'status': 'OK', 'result': send_data})

class GitPgList(generics.ListAPIView):
    serializer_class = GitPgSerializer

    def get(self, request):
        send_data = {}

        return response.Response({'status': 'OK', 'result': send_data})

class GisUgList(generics.ListAPIView):
    serializer_class = GisUgSerializer

    def get(self, request):
        send_data = {}

        return response.Response({'status': 'OK', 'result': send_data})

class GisPgList(generics.ListAPIView):
    serializer_class = GisPgSerializer

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
