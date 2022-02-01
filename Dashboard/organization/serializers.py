from rest_framework import serializers, status
from .models import *


class CampusSerialize(serializers.ModelSerializer):
    institutes = serializers.SerializerMethodField('_institutes')

    def _institutes(self, obj):
        res = []
        insts = Institute.objects.filter(under_campus=obj)
        for i in insts:
            res.append(i.name)
        return res

    class Meta:
        model = Campus
        fields = ('id', 'name', 'inst_count', 'institutes')
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


class StreamsSeralizer(serializers.ModelSerializer):

    class Meta:
        model = Stream
        fields = '__all__'


class CampusSerializeParse(serializers.ModelSerializer):

    class Meta:
        model = Campus
        fields = ['name']


class InstituteSerializeParse(serializers.ModelSerializer):
    campus = serializers.SerializerMethodField('_campus')

    def _campus(self, obj):
        return str(obj.under_campus)

    class Meta:
        model = Institute
        fields = ['name', 'campus']
