from rest_framework import serializers
from .models import Campus, Institue, UnderGraduates, PostGraduates

class CampusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Campus
        fields = ('id','campus_name', 'institue_count','url')

class InstitueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institue
        fields = ('id','institute_name', 'under_campus','url')

class GraduatesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UnderGraduates
        fields = (
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
            'under_institute',
            'url'
        )

class UnderGraduatesSerializer(GraduatesSerializer):
    pass
class PostGraduatesSerializer(GraduatesSerializer):
    pass