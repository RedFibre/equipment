# Generated by Django 4.2.2 on 2023-08-18 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equ', '0043_organisation'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='organisation_id',
            field=models.IntegerField(null=True),
        ),
    ]