# Generated by Django 4.2.2 on 2023-08-27 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equ', '0047_remove_lab_organisation_lab_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
            ],
        ),
    ]
