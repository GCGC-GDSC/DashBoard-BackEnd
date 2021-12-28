from rest_framework import serializers
from .models import (Courses, Company, CompanyCousesPlaced, Git_ug, Gis_ug, Git_pg, Gis_pg, Pharmacy, Gim_BBA_BCOM, Gim_MBA)

class InstitueLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyCousesPlaced
        fields = '__all__'

class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

"""class CourseCompanySerializer(serializers.Serializer):
    course = CoursesSerializer(many=True)
    company = CompanySerializer(many=True)"""

"""class GitUgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Git_ug
        fields = ('id', 'name_of_the_company', 'profile_offered', 'package', 'CSE', 'IT', 'ECE', 'EEE', 'Mech', 'Civil', 'Bio', 'total_no_of_seats')

class GitPgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Git_pg
        fields = ('id', 'name_of_the_company', 'profile_offered', 'package', 'CST', 'CFIS', 'DS', 'VSLI', 'PSA', 'MD', 'MTA')

class GisPgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gis_pg
        fields = ('id', 'name_of_the_company', 'profile_offered', 'package',
                  'MSc_chemistry_analytics',
                  'MSc_chemistry_organic',
                  'Computer_Science_MCA_3years',
                  'Computer_Science_MCA_2years',
                  'Biotechnology_MSc',
                  'Microbiology_MSc',
                  'Food_Science_Technology_MSc',
                  'Math_MSc',
                  'Math_MSc_Statistics',
                  'BioChemisty_Msc',
                  'Enviromental_MSc',
                  'Physics_and_Electronics_MSc',
                  'Physics_and_Electronics_MPC',
                  'Physics_and_Electronics_MPCS',
                  'Physics_and_Electronics_MECS',
                  'Interg_Biotecchnology_MSc',
                  'total')

class GisUgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gis_ug
        fields = ('id', 'name_of_the_company', 'profile_offered', 'package',
                  'BSc_Chemistry_Honors',
                  'Computer_Science_BCA',
                  'Food_Science_Technology_BSc_Hons',
                  'Math_BSc',
                  'Enviromental_BEM',
                  'BioTechnology_BSc',
                  'total')

class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = ('id', 'name_of_the_company', 'profile_offered', 'package',
                  "B_Pharmacy",
                  "M_Pharmacy_Pharmaceutical_Analysis",
                  "M_Pharmacy_Pharmacology",
                  "M_Pharmacy_Quality_Assurance",
                  "M_Pharmacy_Pharmaceutical_Chemistry",
                  "M_Pharmacy_Pharmaceutics",
                  'total')

class Gim_BBA_BCOMSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gim_BBA_BCOM
        fields = ('id', 'name_of_the_company', 'profile_offered', 'package',
                  'BBA',
                    'BCOM',
                    'BBA_Logistics',
                    'BBA_Business_Analytics',
                    'total')

class Gim_MBASerializer(serializers.ModelSerializer):
    class Meta:
        model = Gim_MBA
        fields = ('id', 'name_of_the_company', 'profile_offered', 'package',
                  'MBA_Finance',
                  'MBA_HR',
                  'MBA_Marketing',
                  'MBA_IB',
                  'MBA',
                  'total')"""