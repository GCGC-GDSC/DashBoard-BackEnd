from rest_framework import serializers, status
from organization.models import Institute
from .models import Graduates
from django.db.models import Q, Count, Max, Sum, Min, Avg
from math import *

map = {
    'git': 'GIT',
    'gim': 'GIM',
    'gis': 'GIS',
    'gsoa': 'GSoA',
    'gin': 'GIN',
    'gip': 'GIP',
    'gsol': 'GSoL',
    'gsgs': 'GSGS',
    'soth': 'SoTH',
    'hbs': 'HBS',
    'soph': 'SoPH',
    'sosh': 'SoSH',
    'sotb': 'SoTB',
    'sosp': 'SoSP',
    'gsbb': 'GSBB',
}


class GraduatesSerializer(serializers.ModelSerializer):

    Percentage_of_students_opted_HS_to_the_total_number = serializers.SerializerMethodField(
        '_Percentage_of_students_opted_HS_to_the_total_number')
    Percentage_of_students_having_backlogs_to_the_total_number_of_students = serializers.SerializerMethodField(
        '_Percentage_of_students_having_backlogs_to_the_total_number_of_students'
    )
    Percentage_of_students_eligible_for_and_requiring_placement = serializers.SerializerMethodField(
        '_Percentage_of_students_eligible_for_and_requiring_placement')
    Percentage_of_students_placed_out_of_eligible_students = serializers.SerializerMethodField(
        '_Percentage_of_students_placed_out_of_eligible_students')
    Percentage_of_students_yet_to_be_placed_out_of_eligible_students = serializers.SerializerMethodField(
        '_Percentage_of_students_yet_to_be_placed_out_of_eligible_students')
    under_institute_name = serializers.SerializerMethodField(
        '_under_institute_name')

    def _under_institute_name(self, i):
        try:
            return map[i.under_institute_name]
        except:
            return "instutenot found"

    def _Percentage_of_students_opted_HS_to_the_total_number(self, i):
        try:
            return round((
                (i.total_opted_for_higher_studies_only / i.total_final_years) *
                100), 2)
        except:
            return 0

    def _Percentage_of_students_having_backlogs_to_the_total_number_of_students(
            self, i):
        try:
            return round(((i.total_backlogs / i.total_final_years) * 100), 2)
        except:
            return 0

    def _Percentage_of_students_eligible_for_and_requiring_placement(self, i):
        try:
            return round(
                ((i.total_students_eligible / i.total_final_years) * 100), 2)
        except:
            return 0

    def _Percentage_of_students_placed_out_of_eligible_students(self, i):
        try:
            return round(((i.total_placed / i.total_students_eligible) * 100),
                         2)
        except:
            return 0

    def _Percentage_of_students_yet_to_be_placed_out_of_eligible_students(
            self, i):
        try:
            return round(
                ((i.total_yet_to_place / i.total_students_eligible) * 100), 2)
        except:
            return 0

    class Meta:
        model = Graduates
        fields = (
            'id', 'under_institute_name', 'under_campus_name',
            'total_students', 'total_final_years',
            'total_higher_study_and_pay_crt',
            'total_opted_for_higher_studies_only',
            'total_not_intrested_in_placments',
            'total_backlogs_opted_for_placements',
            'total_backlogs_opted_for_higherstudies',
            'total_backlogs_opted_for_other_career_options', 'total_backlogs',
            'total_students_eligible', 'total_offers', 'total_multiple_offers',
            'total_placed', 'total_yet_to_place', 'highest_salary',
            'average_salary', 'lowest_salary',
            'Percentage_of_students_opted_HS_to_the_total_number',
            'Percentage_of_students_having_backlogs_to_the_total_number_of_students',
            'Percentage_of_students_eligible_for_and_requiring_placement',
            'Percentage_of_students_placed_out_of_eligible_students',
            'Percentage_of_students_yet_to_be_placed_out_of_eligible_students',
            'is_ug')


class UpdateGraduatesSerializer(serializers.ModelSerializer):

    Percentage_of_students_opted_HS_to_the_total_number = serializers.SerializerMethodField(
        '_Percentage_of_students_opted_HS_to_the_total_number')
    Percentage_of_students_having_backlogs_to_the_total_number_of_students = serializers.SerializerMethodField(
        '_Percentage_of_students_having_backlogs_to_the_total_number_of_students'
    )
    Percentage_of_students_eligible_for_and_requiring_placement = serializers.SerializerMethodField(
        '_Percentage_of_students_eligible_for_and_requiring_placement')
    Percentage_of_students_placed_out_of_eligible_students = serializers.SerializerMethodField(
        '_Percentage_of_students_placed_out_of_eligible_students')
    Percentage_of_students_yet_to_be_placed_out_of_eligible_students = serializers.SerializerMethodField(
        '_Percentage_of_students_yet_to_be_placed_out_of_eligible_students')

    def _Percentage_of_students_opted_HS_to_the_total_number(self, i):
        try:
            return round((
                (i.total_opted_for_higher_studies_only / i.total_final_years) *
                100), 2)
        except:
            return 0

    def _Percentage_of_students_having_backlogs_to_the_total_number_of_students(
            self, i):
        try:
            return round(((i.total_backlogs / i.total_final_years) * 100), 2)
        except:
            return 0

    def _Percentage_of_students_eligible_for_and_requiring_placement(self, i):
        try:
            return round(
                ((i.total_students_eligible / i.total_final_years) * 100), 2)
        except:
            return 0

    def _Percentage_of_students_placed_out_of_eligible_students(self, i):
        try:
            return round(((i.total_placed / i.total_students_eligible) * 100),
                         2)
        except:
            return 0

    def _Percentage_of_students_yet_to_be_placed_out_of_eligible_students(
            self, i):
        try:
            return round(
                ((i.total_yet_to_place / i.total_students_eligible) * 100), 2)
        except:
            return 0

    class Meta:
        model = Graduates
        fields = (
            'id',
            'total_students',
            'total_final_years',
            'total_higher_study_and_pay_crt',
            'total_opted_for_higher_studies_only',
            'total_not_intrested_in_placments',
            'total_backlogs_opted_for_placements',
            'total_backlogs_opted_for_higherstudies',
            'total_backlogs_opted_for_other_career_options',
            'total_students_eligible',
            'total_backlogs',
            'total_offers',
            'total_multiple_offers',
            'total_placed',
            'total_yet_to_place',
            'highest_salary',
            'average_salary',
            'lowest_salary',
            'Percentage_of_students_opted_HS_to_the_total_number',
            'Percentage_of_students_having_backlogs_to_the_total_number_of_students',
            'Percentage_of_students_eligible_for_and_requiring_placement',
            'Percentage_of_students_placed_out_of_eligible_students',
            'Percentage_of_students_yet_to_be_placed_out_of_eligible_students',
        )


class CampusGradListSeralizer(serializers.ModelSerializer):
    pass


class InstituteGradListSeralizer(serializers.ModelSerializer):
    student_details = serializers.SerializerMethodField('_student_details')
    placement_details = serializers.SerializerMethodField('_placement_details')
    salary = serializers.SerializerMethodField('_salary')

    def _student_details(self, obj):
        return {
            "total_students":
            obj.total_students,
            "total_final_years":
            obj.total_final_years,
            "total_backlogs":
            obj.total_backlogs,
            "total_higher_study_and_pay_crt":
            obj.total_higher_study_and_pay_crt,
            "total_opted_for_higher_studies_only":
            obj.total_opted_for_higher_studies_only,
            "total_students_eligible":
            obj.total_students_eligible,
            "total_not_intrested_in_placments":
            obj.total_not_intrested_in_placments,
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


class GBstatsSerializer(serializers.ModelSerializer):
    student_details = serializers.SerializerMethodField('_student_details')
    placement_details = serializers.SerializerMethodField('_placement_details')
    salary = serializers.SerializerMethodField('_salary')

    def _student_details(self, obj):

        total_final_years = Graduates.objects.filter(id__in=obj).aggregate(
            Sum('total_final_years'))['total_final_years__sum']
        total_higher_study_and_pay_crt = Graduates.objects.filter(
            id__in=obj).aggregate(Sum('total_higher_study_and_pay_crt')
                                  )['total_higher_study_and_pay_crt__sum']
        total_opted_for_higher_studies_only = Graduates.objects.filter(
            id__in=obj).aggregate(Sum('total_opted_for_higher_studies_only')
                                  )['total_opted_for_higher_studies_only__sum']
        total_not_intrested_in_placments = Graduates.objects.filter(
            id__in=obj).aggregate(Sum('total_not_intrested_in_placments')
                                  )['total_not_intrested_in_placments__sum']
        total_backlogs_opted_for_placements = Graduates.objects.filter(
            id__in=obj).aggregate(Sum('total_backlogs_opted_for_placements')
                                  )['total_backlogs_opted_for_placements__sum']

        total_not_intrested_in_placments = Graduates.objects.filter(
            id__in=obj).aggregate(Sum('total_not_intrested_in_placments')
                                  )['total_not_intrested_in_placments__sum']


        total_backlogs_opted_for_higherstudies = Graduates.objects.filter(
            id__in=obj).aggregate(
                sum=Sum('total_backlogs_opted_for_higherstudies')).get('sum')
        total_backlogs_opted_for_placements = Graduates.objects.filter(
            id__in=obj).aggregate(
                sum=Sum('total_backlogs_opted_for_placements')).get('sum')
        total_backlogs_opted_for_other_career_options = Graduates.objects.filter(
            id__in=obj).aggregate(sum=Sum(
                'total_backlogs_opted_for_other_career_options')).get('sum')

        serializer = (Graduates.objects.filter(id__in=obj).aggregate(
            total_students=Sum('total_students'),
            total_final_years=Sum('total_final_years'),
            total_higher_study_and_pay_crt=Sum(
                'total_higher_study_and_pay_crt')))
        serializer.update({
            'total_backlogs': (total_backlogs_opted_for_higherstudies +
                               total_backlogs_opted_for_other_career_options +
                               total_backlogs_opted_for_placements),
            'total_students_eligible': (total_final_years -
                                   total_higher_study_and_pay_crt -
                                   total_opted_for_higher_studies_only -
                                   total_not_intrested_in_placments -
                                   total_backlogs_opted_for_placements),
            'total_not_intrested_in_placments':(Graduates.objects.filter(id__in=obj).aggregate(
            total_not_intrested_in_placments=Sum(
                total_not_intrested_in_placments)
            ))['total_not_intrested_in_placments'],
             "total_opted_for_higher_studies_only": total_opted_for_higher_studies_only,
        })
        return serializer


    def _placement_details(self, obj):
        total_final_years = Graduates.objects.filter(id__in=obj).aggregate(
            Sum('total_final_years'))['total_final_years__sum']
        total_backlogs_opted_for_higherstudies = Graduates.objects.filter(
            id__in=obj).aggregate(
                Sum('total_backlogs_opted_for_higherstudies'
                    ))['total_backlogs_opted_for_higherstudies__sum']
        total_backlogs_opted_for_placements = Graduates.objects.filter(
            id__in=obj).aggregate(Sum('total_backlogs_opted_for_placements')
                                  )['total_backlogs_opted_for_placements__sum']
        total_backlogs_opted_for_other_career_options = Graduates.objects.filter(
            id__in=obj).aggregate(
                Sum('total_backlogs_opted_for_other_career_options')
            )['total_backlogs_opted_for_other_career_options__sum']
        total_backlogs = (total_backlogs_opted_for_higherstudies +
                          total_backlogs_opted_for_other_career_options +
                          total_backlogs_opted_for_placements)
        total_not_intrested_in_placments = Graduates.objects.filter(
            id__in=obj).aggregate(Sum('total_not_intrested_in_placments')
                                  )['total_not_intrested_in_placments__sum']
        total_offers = Graduates.objects.filter(id__in=obj).aggregate(
            Sum('total_offers'))['total_offers__sum']
        total_multiple_offers = Graduates.objects.filter(id__in=obj).aggregate(
            Sum('total_multiple_offers'))['total_multiple_offers__sum']
        total_higher_study_and_pay_crt = Graduates.objects.filter(
            id__in=obj).aggregate(Sum('total_higher_study_and_pay_crt')
                                  )['total_higher_study_and_pay_crt__sum']
        total_opted_for_higher_studies_only = Graduates.objects.filter(
            id__in=obj).aggregate(Sum('total_opted_for_higher_studies_only')
                                  )['total_opted_for_higher_studies_only__sum']
        total_students_eligible = (total_final_years -
                                   total_higher_study_and_pay_crt -
                                   total_opted_for_higher_studies_only -
                                   total_not_intrested_in_placments -
                                   total_backlogs_opted_for_placements)

        serializer = (Graduates.objects.filter(id__in=obj).aggregate(
            total_not_intrested_in_placments=Sum(
                total_not_intrested_in_placments),
            total_offers=Sum(total_offers),
            total_multiple_offers=Sum(total_multiple_offers)))

        serializer.update({
            "placed": (total_offers - total_multiple_offers),
            "yet_to_place":
            (total_students_eligible - (total_offers - total_multiple_offers)),
            "total_students_eligible":
            total_students_eligible,
            "total_opted_for_higher_studies_only": total_opted_for_higher_studies_only,
        })

        return serializer

    def _salary(self, obj):
        return (Graduates.objects.filter(id__in=obj).aggregate(
            highest=Max("highest_salary"),
            average=Avg("average_salary"),
            lowest=Min("lowest_salary")))

    class Meta:
        model = Graduates
        fields = ['student_details', 'placement_details', 'salary', 'is_ug']
