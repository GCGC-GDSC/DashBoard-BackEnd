from rest_framework import generics, status, views, response
from .models import *
from .serializers import *
from django.contrib.auth.models import User, auth

class Authenticate(views.APIView):
    serializer_class = AccountSerialize
    def post(self,request,email,format=None):
        try:
            qs = Accounts.objects.get(email=email)
        except:
            return response.Response({'status':'error','result':'email not verified'})
        
        send_data = []        
        send_data = (AccountSerialize(qs).data)

        return response.Response({'status':'OK',"result":send_data})