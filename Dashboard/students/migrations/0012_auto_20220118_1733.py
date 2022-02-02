# Generated by Django 3.2.8 on 2022-01-18 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0011_alter_graduates_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graduates',
            name='total_backlogs',
        ),
        migrations.AddField(
            model_name='graduates',
            name='total_backlogs_opted_for_higherstudies',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='graduates',
            name='total_backlogs_opted_for_other_career_options',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='graduates',
            name='total_backlogs_opted_for_placements',
            field=models.IntegerField(default=0),
        ),
    ]