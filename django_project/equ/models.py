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


class Profile(models.Model):
    USER_TYPES = [
        ('Student', 'Student'),
        ('Professor', 'Professor'),
        ('Technician', 'Technician'),
        ('Other', 'Outsider'),
    ]

    MACHINE_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    HOW_HEARD_CHOICES = [
        ('Peers', 'Peers'),
        ('Faculty', 'Faculty'),
        ('Technicians', 'Technicians'),
        ('Social Media', 'Social Media'),
        ('Campus Communication', 'Campus Communication'),
        ('Others', 'Others'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    branch = models.CharField(max_length=100)
    year_of_graduation = models.PositiveIntegerField(blank=True, null=True)
    institute_name = models.CharField(max_length=100)
    training_record = models.CharField(max_length=3, choices=MACHINE_CHOICES)
    machines_trained_in = models.CharField(max_length=200, blank=True)
    how_heard_about = models.CharField(max_length=50, choices=HOW_HEARD_CHOICES, blank=True, null=True)



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
    CONDITION_CHOICES = [
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Poor', 'Poor'),
        ('Bad', 'Bad'),
    ]
    name = models.CharField(max_length=100)
    lab = models.ForeignKey('Lab', on_delete=models.CASCADE, related_name='equipments')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='Good')
    
    def __str__(self):
        return self.name
    

    
class Booking(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
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
    project = models.ForeignKey(Archived_Project, on_delete=models.CASCADE, null=True, blank=True,default=None)

    def __str__(self):
        return f'{self.start_time} - {self.end_time} for {self.equipment}'
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    lab = models.ForeignKey(Lab,on_delete=models.CASCADE)

  
class Material(models.Model):
    stock = models.IntegerField(null=True,blank=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.name
    
class Material_Request(models.Model):
    REQUEST_TYPES = [
        ('_', '_'),
        ('Borrow', 'Borrow'),
        ('Issue', 'Issue'),
    ]

    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPES)
    return_date = models.DateField(null=True, blank=True)  # Set only for issue requests
    status = models.IntegerField(default=0) #0-pending, 1-active, 2-closed
    user = models.ForeignKey(User,on_delete=models.CASCADE)