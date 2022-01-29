from rest_framework import serializers, status
from .models import *

class AccountSerialize(serializers.ModelSerializer):
    campus = serializers.SerializerMethodField('_campus')
    institute = serializers.SerializerMethodField('_institute')


    def _campus(self,obj):
        return str(obj.campus)
    
    def _institute(self,obj):
        return str(obj.institute)

    class Meta:
        model = Accounts
        fields = ['id','eid','name','email','can_edit','campus','institute','ug_pg']