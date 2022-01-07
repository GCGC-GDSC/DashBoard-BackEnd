from rest_framework import serializers
from .models import (Company, Courses, CompanyCousesPlaced)
from students.models import (
    Institute, )
from organization.serializers import CompanySeralizer


class CompanyCousesPlacedSeralizer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField('_course_name')
    is_ug = serializers.SerializerMethodField('_is_ug')

    def _course_name(self, obj):
        return obj.course.course

    def _is_ug(self, obj):
        return obj.course.is_ug

    class Meta:
        model = CompanyCousesPlaced
        fields = ['id', 'course_name', 'selected', 'is_ug']


class CompanySeralizer(serializers.ModelSerializer):
    course = CompanyCousesPlacedSeralizer(source='companycousesplaced_set',
                                          many=True)

    class Meta:
        model = Company
        fields = [
            'id', 'name_of_the_company', 'profile_offered', 'package', 'course'
        ]


class InstituteLevelSeralizer(serializers.ModelSerializer):
    campus = serializers.SerializerMethodField('_campus')
    institue = serializers.SerializerMethodField('_institue')

    companies = CompanySeralizer(many=True, read_only=True)

    def _campus(self, obj):
        return obj.under_campus.name

    def _institue(self, obj):
        return obj.name

    class Meta:
        model = Institute
        fields = ['id', 'institue', 'campus', 'companies']
