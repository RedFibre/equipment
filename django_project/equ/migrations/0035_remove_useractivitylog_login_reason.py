# Generated by Django 4.2.2 on 2023-08-11 03:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equ', '0034_alter_equipment_condition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useractivitylog',
            name='login_reason',
        ),
    ]