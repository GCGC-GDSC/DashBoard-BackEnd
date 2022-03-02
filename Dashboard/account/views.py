from rest_framework import generics, status, views, response
from .models import *
from .serializers import *
from django.contrib.auth.models import User, auth
from rest_framework.status import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()


class Authenticate(views.APIView):
    serializer_class = UserSerialize

    def post(self, request, email, format=None):     
        try:
            qs = User.objects.get(email=email)
        except:
            return response.Response(
                {
                    'status': 'error',
                    'result': 'Email is not verified'
                },
                status=HTTP_423_LOCKED)

        send_data = []
        try:
            send_data = UserSerialize(qs).data
            account_obj = User.objects.get(eid=qs.eid)
            account_token = Token.objects.get(user=account_obj.id)
            send_data['token'] = TokenSerialiazer(account_token).data
        except Exception as e:
            return response.Response({
                'status': 'Error',
                'result': str(e)
            },
                                     status=HTTP_500_INTERNAL_SERVER_ERROR)
        return response.Response({'status': 'OK', "result": send_data})


class GetTokenOfUser(views.APIView):

    def post(self, request, eid, format=None):
        send_data = {}
        try:
            account_obj = User.objects.get(eid=eid)
            account_token = Token.objects.get(user=account_obj.id)
            send_data = TokenSerialiazer(account_token).data
        except:
            return response.Response({
                'status': 'Error',
                result: str(e)
            },
                                     status=HTTP_500_INTERNAL_SERVER_ERROR)

        return response.Response({'status': 'OK', "result": send_data})
