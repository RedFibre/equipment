from django.contrib import admin
from .models import Lab,Project,Equipment,Booking,UserLab


admin.site.register(Lab)
admin.site.register(Project)
admin.site.register(Equipment)
admin.site.register(Booking)
admin.site.register(UserLab)


