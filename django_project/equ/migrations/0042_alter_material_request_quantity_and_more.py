# Generated by Django 4.2.2 on 2023-08-14 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equ', '0041_alter_material_request_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material_request',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='material_request',
            name='request_type',
            field=models.CharField(choices=[('_', '_'), ('Borrow', 'Borrow'), ('Issue', 'Issue')], max_length=10),
        ),
    ]
