from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_redirect, name='user_redirect'),
    path('a_overview/',views.a_overview,name="a_overview"),
    path('a_members/',views.a_members,name="a_members"),
    path('a_equipment/',views.a_equipment,name="a_equipment"),
    path('a_activity/',views.a_activity,name="a_activity"),
    path('a_project_detail/<int:pk>/', views.a_project_detail, name='a_project_detail'),
    path('c_list/',views.c_list,name="c_list"),
    path('u_projects/',views.u_projects,name="u_projects"),
    path('u_help/',views.u_help,name="u_help"),
    path('u_settings/',views.u_settings,name="u_settings"),
    path('s_overview/', views.s_overview, name='s_overview'),
    path('s_labs/', views.s_labs, name='s_labs'),
    path('s_admins/', views.s_admins, name='s_admins'),
    path('s_projects/', views.s_projects, name='s_projects'),
    path('s_equipment/', views.s_equipment, name='s_equipment'),
    path('u_create_project/', views.u_create_project, name='u_create_project'),
    path('u_project_detail/<int:pk>/', views.u_project_detail, name='u_project_detail'),
    path('c_m1/<int:pk>/', views.c_m1, name='c_m1'),
    path('c_m2/<int:pk>/', views.c_m2, name='c_m2'),
    path('c_m3/<int:pk>/', views.c_m3, name='c_m3'),
    path('u_confirmed_project_detail/<int:pk>/', views.u_confirmed_project_detail, name='u_confirmed_project_detail'),
]