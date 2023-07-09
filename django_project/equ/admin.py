from django.contrib import admin
from .models import Lab,Project,Equipment,Booking,UserLab,Material,Confirmed_Booking,Confirmed_Project


admin.site.register(Lab)
admin.site.register(Project)
admin.site.register(Equipment)
admin.site.register(Booking)
admin.site.register(UserLab)
admin.site.register(Material)
admin.site.register(Confirmed_Project)
admin.site.register(Confirmed_Booking)



