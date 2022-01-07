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


class CoursesSeralizer(serializers.ModelSerializer):
    campus_name = serializers.SerializerMethodField('_course_name')
    institute_name = serializers.SerializerMethodField('_institute_name')

    def _course_name(self, obj):
        return obj.campus.name

    def _institute_name(self, obj):
        return obj.institute.name

    class Meta:
        model = Courses
        fields = ['id', 'course', 'is_ug', 'campus_name', 'institute_name']
