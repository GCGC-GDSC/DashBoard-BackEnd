# Generated by Django 3.2.8 on 2021-12-25 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_auto_20211028_1226'),
        ('company', '0002_auto_20211225_1727'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(default='', max_length=10)),
                ('campus', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='students.campus')),
                ('institute', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='students.institute')),
            ],
        ),
    ]