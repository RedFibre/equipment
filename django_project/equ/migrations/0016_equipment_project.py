# Generated by Django 4.2.2 on 2023-06-23 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equ', '0015_equipment_usage'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='project',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='equ.project'),
        ),
    ]
