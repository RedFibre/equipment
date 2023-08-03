from django.contrib import admin
from .models import Lab,Project,Equipment,Booking,Material,UserActivityLog
from .models import Confirmed_Booking,Confirmed_Project,Archived_Project,Archived_Booking,Notification,Profile

admin.site.register(Lab)
admin.site.register(Project)
admin.site.register(Equipment)
admin.site.register(Booking)
admin.site.register(Material)
admin.site.register(Confirmed_Project)
admin.site.register(Confirmed_Booking)
admin.site.register(Archived_Project)
admin.site.register(Archived_Booking)
admin.site.register(Notification)
admin.site.register(Profile)
admin.site.register(UserActivityLog)



