from django.contrib import admin
from .models import Lab,Project,Equipment,TimeSlot,UserLab


admin.site.register(Lab)
admin.site.register(Project)
admin.site.register(Equipment)
admin.site.register(TimeSlot)
admin.site.register(UserLab)


