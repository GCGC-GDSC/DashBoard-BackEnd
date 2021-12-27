from rest_framework import serializers, status
from .models import *


class CampusSerialize(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ('id', 'name', 'inst_count')
        ordering = ['-id']


class InstituteSerialize(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = ('id', 'name', 'campus_name')
        ordering = ['-under_campus']


class GraduatesSerialize(serializers.ModelSerializer):
    class Meta:
        model = Graduates
        fields = (
            'under_institute_name',
            'under_campus_name',
            'total_students',
            'total_final_years',
            'total_higher_study_and_pay_crt',
            'total_not_intrested_in_placments',
            'total_backlogs',
            'total_students_eligible',
            'total_offers',
            'total_multiple_offers',
            'total_placed',
            'total_yet_to_place',
            'highest_salary',
            'average_salary',
            'lowest_salary',
            'is_ug'
        )
