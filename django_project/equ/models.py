from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    lab = models.ForeignKey('Lab', on_delete=models.CASCADE, related_name='projects')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipments = models.ManyToManyField('Equipment', related_name='projects', blank=True)

    def __str__(self):
        return self.name



class Equipment(models.Model):
    name = models.CharField(max_length=100)
    lab = models.ForeignKey('Lab', on_delete=models.CASCADE, related_name='equipments')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True,default=None)
    
    def __str__(self):
        return self.name

class Request(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.start_time} - {self.end_time} for {self.equipment}' 

    
class TimeSlot(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.start_time} - {self.end_time} for {self.equipment}'

class Lab(models.Model):
    name = models.CharField(max_length=100)
    lab_admin = models.ForeignKey(
        User,
        limit_choices_to={'groups__name': 'admin'},
        null=True,  # Set the default value to None
        on_delete=models.CASCADE,
        related_name='lab_admin_of'
    )

    def __str__(self):
        return self.name
    
class UserLab(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.lab}'
