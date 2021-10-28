# Generated by Django 3.2.8 on 2021-10-15 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_alter_institute_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Graduates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_students', models.IntegerField(default=0)),
                ('total_final_years', models.IntegerField(default=0)),
                ('total_higher_study_and_pay_crt', models.IntegerField(default=0)),
                ('total_not_intrested_in_placments', models.IntegerField(default=0)),
                ('total_backlogs', models.IntegerField(default=0)),
                ('total_offers', models.IntegerField(default=0)),
                ('total_multiple_offers', models.IntegerField(default=0)),
                ('highest_salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('average_salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('lowest_salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('is_pg', models.BooleanField(default=False)),
                ('under_campus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.campus')),
                ('under_institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.institute')),
            ],
        ),
    ]
