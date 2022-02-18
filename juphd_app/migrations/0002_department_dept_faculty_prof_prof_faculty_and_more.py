# Generated by Django 4.0.2 on 2022-02-18 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juphd_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='dept_faculty',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='prof',
            name='prof_faculty',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='student_faculty',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
