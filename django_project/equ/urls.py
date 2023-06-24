from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_redirect, name='user_redirect'),
    path('home/',views.home,name="home"),
    path('calendar/',views.calendar,name="calendar"),
    path('members/',views.members,name="members"),
    path('equipment/',views.equipment,name="equipment"),
    path('activity/',views.activity,name="activity"),
    path('inventory/',views.inventory,name="inventory"),
    path('calendaruser/',views.calendaruser,name="calendaruser"),
    path('projects/',views.projects,name="projects"),
    path('help/',views.help,name="help"),
    path('settings/',views.settings,name="settings"),
    path('superoverview/', views.superoverview, name='superoverview'),
    path('superlabs/', views.superlabs, name='superlabs'),
    path('superadmins/', views.superadmins, name='superadmins'),
    path('superprojects/', views.superprojects, name='superprojects'),
    path('superequipments/', views.superequipments, name='superequipments'),
    path('superinventory/', views.superinventory, name='superinventory'),
    path('create_project/', views.create_project, name='create_project'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('lab/<int:pk>/calendar/', views.labcalendar, name='labcalendar'),
    
]