# Generated by Django 3.2.8 on 2022-02-05 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelData',
            fields=[
                ('id',
                 models.BigAutoField(auto_created=True,
                                     primary_key=True,
                                     serialize=False,
                                     verbose_name='ID')),
                ('uploadedFile', models.FileField(upload_to='UploadedFiles/')),
            ],
        ),
        migrations.CreateModel(
            name='Graduates',
            fields=[
                ('id',
                 models.BigAutoField(auto_created=True,
                                     primary_key=True,
                                     serialize=False,
                                     verbose_name='ID')),
                ('total_students', models.IntegerField(default=0)),
                ('total_final_years', models.IntegerField(default=0)),
                ('total_higher_study_and_pay_crt',
                 models.IntegerField(default=0)),
                ('total_opted_for_higher_studies_only',
                 models.IntegerField(default=0)),
                ('total_not_intrested_in_placments',
                 models.IntegerField(default=0)),
                ('total_backlogs_opted_for_placements',
                 models.IntegerField(default=0)),
                ('total_backlogs_opted_for_higherstudies',
                 models.IntegerField(default=0)),
                ('total_backlogs_opted_for_other_career_options',
                 models.IntegerField(default=0)),
                ('total_offers', models.IntegerField(default=0)),
                ('total_multiple_offers', models.IntegerField(default=0)),
                ('highest_salary',
                 models.DecimalField(decimal_places=2,
                                     default=0.0,
                                     max_digits=5)),
                ('average_salary',
                 models.DecimalField(decimal_places=2,
                                     default=0.0,
                                     max_digits=5)),
                ('lowest_salary',
                 models.DecimalField(decimal_places=2,
                                     default=0.0,
                                     max_digits=5)),
                ('is_ug', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('under_campus',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='organization.campus')),
                ('under_institute',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='organization.institute')),
            ],
        ),
    ]
