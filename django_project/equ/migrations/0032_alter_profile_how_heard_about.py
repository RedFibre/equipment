# Generated by Django 4.2.2 on 2023-08-11 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equ', '0031_alter_profile_lab'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='how_heard_about',
            field=models.CharField(blank=True, choices=[('Peers', 'Peers'), ('Faculty', 'Faculty'), ('Technicians', 'Technicians'), ('Social Media', 'Social Media'), ('Campus Communication', 'Campus Communication'), ('Others', 'Others')], max_length=50, null=True),
        ),
    ]
