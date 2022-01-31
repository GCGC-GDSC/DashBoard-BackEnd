from rest_framework import serializers, status
from .models import *
from organization.serializers import *
from organization.models import *

class AccountSerialize(serializers.ModelSerializer):
    campus = serializers.SerializerMethodField('_campus_name')
    institute = serializers.SerializerMethodField('_institute_name')
    grad = serializers.SerializerMethodField('_grad_level')
    role = serializers.SerializerMethodField('_role_name')
    
    def _campus_name(self,obj):
        try:
            qs = AccountsCampusLevel.objects.get(accounts_ptr=obj)
            return [str(qs.campus)]
        except:
            qs = CampusSerializeParse(Campus.objects.all(),many=True).data
            return qs
    
    def _institute_name(self,obj):
        try:
            qs = AccountsInstituteLevel.objects.get(accounts_ptr=obj)
            return [str(qs.institute)]
        except:
            qs = InstituteSerializeParse(Institute.objects.all(),many=True).data
            return qs
    def _grad_level(self,obj):
        try:
            qs = AccountsGraduationLevel.objects.get(accounts_ptr=obj)
            return [str(qs.grad)]
        except:
            return ["ug","pg"]

    def _role_name(self,obj):
        try:
            qs = AccountsHead.objects.get(accounts_ptr=obj)
            return str(qs.role)
        except:
            return "general"
    

    class Meta:
        model = Accounts
        fields = '__all__'