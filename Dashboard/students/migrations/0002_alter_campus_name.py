# Generated by Django 3.2.8 on 2021-10-15 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campus',
            name='name',
            field=models.CharField(default='', max_length=30, unique=True),
        ),
    ]