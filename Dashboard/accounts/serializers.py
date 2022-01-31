from rest_framework import serializers, status
from .models import *
from organization.serializers import *
from organization.models import *
'''
class AccountSerialize(serializers.ModelSerializer):
    campus = serializers.SerializerMethodField('_campus_name')
    institute = serializers.SerializerMethodField('_institute_name')
    grad = serializers.SerializerMethodField('_grad_level')
    role = serializers.SerializerMethodField('_role_name')
    
    def _campus_name(self,obj):
        try:
            qs = AccountsCampusLevel.objects.get(accounts_ptr=obj)
            return [{'name':str(qs.campus)}]
        except:
            qs = CampusSerializeParse(Campus.objects.all(),many=True).data
            return qs
    
    def _institute_name(self,obj):
        try:
            qs = AccountsInstituteLevel.objects.get(accounts_ptr=obj)
            return [{'name':str(qs.institute),'campus':str(qs.campus)}]
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
'''


class AccountSerialize(serializers.ModelSerializer):
    can_edit = serializers.SerializerMethodField('_can_edit')
    campus = serializers.SerializerMethodField('_campus_name')
    institute = serializers.SerializerMethodField('_institute')

    def _can_edit(self,obj):
        if obj.access=="edit_all" or obj.access=="edit_some":
            return True
        return False
    
    def _campus_name(self,obj):
        if obj.university=="univ":
            return CampusSerializeParse(Campus.objects.all(),many=True).data
        qs = Campus.objects.filter(name=obj.university)
        return CampusSerializeParse(qs,many=True).data
    
    def _institute(self,obj):
        if obj.university!="univ":
            campus = Campus.objects.filter(name=obj.university)
        else:
            return InstituteSerializeParse(Institute.objects.all(),many=True).data

        
        return InstituteSerializeParse(Institute.objects.filter(under_campus__in=campus),many=True).data

    class Meta:
        model = Accounts
        fields = ['id','eid','name','designation','can_edit','campus','institute']
