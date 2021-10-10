from rest_framework import serializers
from .models import Campus, Institue, UnderGraduates, PostGraduates

class CampusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Campus
        fields = ('camp', 'inst_cnt')

class InstitueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institue
        fields = ('inst', 'under_camp')

class UnderGraduatesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UnderGraduates
        fields = ('total_no_of_students', 'total_no_of_final_year_students', 'total_no_of_students_opt_higher_study_and_pay_crt', 'under_inst')

class PostGraduatesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostGraduates
        fields = ('total_no_of_students', 'total_no_of_final_year_students', 'total_no_of_students_opt_higher_study_and_pay_crt', 'under_inst')

