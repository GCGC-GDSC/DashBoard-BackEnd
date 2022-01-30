from rest_framework import serializers, status
from .models import *


class AccountSerialize(serializers.ModelSerializer):
    campus = serializers.SerializerMethodField('_campus_name')
    institute = serializers.SerializerMethodField('_institute_name')
    grad = serializers.SerializerMethodField('_grad_level')
    role = serializers.SerializerMethodField('_role_name')
    
    def _campus_name(self,obj):
        try:
            qs = AccountsCampusLevel.objects.get(accounts_ptr=obj)
            return str(qs.campus)
        except:
            return "all"
    
    def _institute_name(self,obj):
        try:
            qs = AccountsInstituteLevel.objects.get(accounts_ptr=obj)
            print(qs)
            return str(qs.institute)
        except:
            return "all"
    def _grad_level(self,obj):
        try:
            qs = AccountsGraduationLevel.objects.get(accounts_ptr=obj)
            return str(qs.grad)
        except:
            return "all"

    def _role_name(self,obj):
        try:
            qs = AccountsHead.objects.get(accounts_ptr=obj)
            return str(qs.role)
        except:
            return "general"
    

    class Meta:
        model = Accounts
        fields = '__all__'