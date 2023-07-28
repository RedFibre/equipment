from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    lab = models.ForeignKey('Lab', on_delete=models.CASCADE, related_name='projects')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now) 

    def __str__(self): 
        return self.name



class Equipment(models.Model):
    name = models.CharField(max_length=100)
    lab = models.ForeignKey('Lab', on_delete=models.CASCADE, related_name='equipments')
    
    def __str__(self):
        return self.name
    
class Material(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE,null=True,blank=True,default=None)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    materials = models.ManyToManyField(Material)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True,default=None)

    def __str__(self):
        return f'{self.start_time} - {self.end_time} for {self.equipment}'
    

class Confirmed_Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    lab = models.ForeignKey('Lab', on_delete=models.CASCADE, related_name='confirmed_projects')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now) 

    def __str__(self): 
        return self.name
    
class Confirmed_Booking(models.Model): 
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    materials = models.ManyToManyField(Material)
    project = models.ForeignKey(Confirmed_Project, on_delete=models.CASCADE, null=True, blank=True,default=None)

    def __str__(self):
        return f'{self.start_time} - {self.end_time} for {self.equipment}'
    
class Archived_Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    lab = models.ForeignKey('Lab', on_delete=models.CASCADE, related_name='archived_projects')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now) 

    def __str__(self): 
        return self.name
    

class Archived_Booking(models.Model): 
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    materials = models.ManyToManyField(Material)
    project = models.ForeignKey(Archived_Project, on_delete=models.CASCADE, null=True, blank=True,default=None)

    def __str__(self):
        return f'{self.start_time} - {self.end_time} for {self.equipment}'
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message