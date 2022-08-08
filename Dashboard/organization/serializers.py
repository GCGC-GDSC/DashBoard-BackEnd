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
    # campus_name = serializers.SerializerMethodField('_course_name')
    # institute_name = serializers.SerializerMethodField('_institute_name')

    # def _course_name(self, obj):
    #     return obj.campus.name

    # def _institute_name(self, obj):
    #     return obj.institute.name

    class Meta:
        model = Courses
        fields = '__all__'


class ProgramSeralizer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField('_course')

    def _course(self, obj):
        return obj.under_course.course

    class Meta:
        model = Programs
        fields = ['name','course','is_ug']

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
    programs = serializers.SerializerMethodField('_programs')

    def _campus(self, obj):
        return str(obj.under_campus)

    def _programs(self, obj):
        return ProgramSeralizer(Programs.objects.filter(under_institute=obj, under_campus=obj.under_campus), many=True).data

    class Meta:
        model = Institute
        fields = ['name', 'campus', 'programs']
