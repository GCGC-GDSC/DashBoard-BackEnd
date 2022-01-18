from rest_framework import serializers, status
from organization.models import Institute
from .models import Graduates


class GraduatesSerialize(serializers.ModelSerializer):

    class Meta:
        model = Graduates
        fields = ('under_institute_name', 'under_campus_name',
                  'total_students', 'total_final_years',
                  'total_higher_study_and_pay_crt',
                  'total_not_intrested_in_placments', 'total_backlogs',
                  'total_students_eligible', 'total_offers',
                  'total_multiple_offers', 'total_placed',
                  'total_yet_to_place', 'highest_salary', 'average_salary',
                  'lowest_salary', 'is_ug')


class CampusGradListSeralizer(serializers.ModelSerializer):
    pass


class InstituteGradListSeralizer(serializers.ModelSerializer):
    student_details = serializers.SerializerMethodField('_student_details')
    placement_details = serializers.SerializerMethodField('_placement_details')
    salary = serializers.SerializerMethodField('_salary')

    def _student_details(self, obj):
        return {
            "total_students": obj.total_students,
            "total_final_years": obj.total_final_years,
            "total_backlogs": obj.total_backlogs,
            "total_higher_study_and_pay_crt":
            obj.total_higher_study_and_pay_crt
        }

    def _placement_details(self, obj):
        return {
            "total_students_eligible": obj.total_students_eligible,
            "total_not_intrested_in_placments":
            obj.total_not_intrested_in_placments,
            "total_offers": obj.total_offers,
            "placed": obj.total_placed,
            "yet_to_place": obj.total_yet_to_place,
            "total_multiple_offers": obj.total_multiple_offers
        }

    def _salary(self, obj):
        return {
            "highest": obj.highest_salary,
            "average": obj.average_salary,
            "lowest": obj.lowest_salary
        }

    class Meta:
        model = Graduates
        fields = ['student_details', 'placement_details', 'salary', 'is_ug']


class DataUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Graduates
        fields = '__all__'
