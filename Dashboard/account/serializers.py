from rest_framework import serializers, status
from .models import *
from organization.serializers import *
from organization.models import *
from rest_framework.authtoken.models import Token


class UserSerialize(serializers.ModelSerializer):
    can_edit = serializers.SerializerMethodField('_can_edit')
    campus = serializers.SerializerMethodField('_campus_name')
    institute = serializers.SerializerMethodField('_institute')

    def _can_edit(self, obj):
        if obj.access == "edit_all" or obj.access == "edit_some":
            return True
        return False

    def _campus_name(self, obj):
        if obj.university == "univ":
            return CampusSerializeParse(Campus.objects.all(), many=True).data
        qs = Campus.objects.filter(name=obj.university)
        return CampusSerializeParse(qs, many=True).data

    def _institute(self, obj):
        if obj.university != "univ":
            campus = Campus.objects.filter(name=obj.university)
        else:
            return InstituteSerializeParse(Institute.objects.all(),
                                           many=True).data

        return InstituteSerializeParse(
            Institute.objects.filter(under_campus__in=campus), many=True).data

    class Meta:
        model = User
        fields = [
            'id',
            'eid',
            'name',
            'designation',
            'can_edit',
            'campus',
            'institute',
        ]


class TokenSerialiazer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = '__all__'
