from rest_framework import generics, status, views, response
from .models import *
from .serializers import *
from django.contrib.auth.models import User, auth
from rest_framework.status import *


class Authenticate(views.APIView):
    serializer_class = AccountSerialize

    def post(self, request, email, format=None):
        try:
            qs = Accounts.objects.get(email=email)
        except:
            return response.Response(
                {
                    'status': 'error',
                    'result': 'email not verified'
                },
                status=HTTP_423_LOCKED)

        send_data = []
        try:
            send_data = AccountSerialize(qs).data
        except Exception as e:
            return response.Response({
                'status': 'error',
                'result': str(e)
            },
                                     status=HTTP_500_INTERNAL_SERVER_ERROR)
        return response.Response({'status': 'OK', "result": send_data})
