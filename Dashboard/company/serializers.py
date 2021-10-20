from rest_framework import serializers
from .models import Git, Gis

class GitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Git
        fields = ('id', 'name_of_the_company', 'profile_offered', 'package', 'CSE', 'IT', 'ECE', 'EEE', 'Mech', 'Civil', 'Bio')


class GisSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gis
        fields = ('id', 'name_of_the_company', 'profile_offered', 'package',
                  'MSc_chemistry_analytics',
                  'MSc_chemistry_organic',
                  'BSc_Chemistry_Honors',
                  'Computer_Science_BCA',
                  'Computer_Science_MCA_3years',
                  'Computer_Science_MCA_2years',
                  'Biotechnology_MSc',
                  'Microbiology_MSc',
                  'Food_Science_Technology_MSc',
                  'Food_Science_Technology_BSc_Hons',
                  'Math_MSc',
                  'Math_MSc_Statistics',
                  'Math_BSc',
                  'BioChemisty_Msc',
                  'Enviromental_MSc',
                  'Enviromental_BEM',
                  'Physics_and_Electronics_MSc',
                  'Physics_and_Electronics_MPC',
                  'Physics_and_Electronics_MPCS',
                  'Physics_and_Electronics_MECS',
                  'BioTechnology_BSc',
                  'Interg_Biotecchnology_MSc',)
