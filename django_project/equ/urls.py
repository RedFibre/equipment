from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.user_redirect, name='user_redirect'),
    path('a_overview/',views.a_overview,name="a_overview"),
    path('a_members/',views.a_members,name="a_members"),
    path('a_member_detail/<int:pk>/', views.a_member_detail, name='a_member_detail'),
    path('a_equipment/',views.a_equipment,name="a_equipment"),
    path('a_add_equipment/', views.a_add_equipment, name='a_add_equipment'),
    path('a_remove_equipment/<int:pk>/', views.a_remove_equipment, name='a_remove_equipment'),
    path('a_add_material/<int:pk>/', views.a_add_material, name='a_add_material'),
    path('a_add_stock/<int:pk>/', views.a_add_stock, name='a_add_stock'),
    path('a_activity/',views.a_activity,name="a_activity"),
    path('a_project_detail/<int:pk>/', views.a_project_detail, name='a_project_detail'),
    path('a_confirmed_project_detail/<int:pk>/', views.a_confirmed_project_detail, name='a_confirmed_project_detail'),
    path('c_list_superadmin/<int:pk>/',views.c_list_superadmin,name="c_list_superadmin"),
    path('c_list/',views.c_list,name="c_list"),
    path('u_projects/',views.u_projects,name="u_projects"),
    path('u_help/',views.u_help,name="u_help"),
    path('u_settings/',views.u_settings,name="u_settings"),
    path('u_profile/', views.u_profile, name='u_profile'),
    path('u_profilepage/', views.u_profile_page, name='u_profile_page'),
    path('s_overview/', views.s_overview, name='s_overview'),
    path('s_labs/', views.s_labs, name='s_labs'),
    path('s_lab_detail/<int:pk>/', views.s_lab_detail, name='s_lab_detail'),
    path('s_member_detail/<int:pk>/', views.s_member_detail, name='s_member_detail'),
    path('s_confirmed_project_detail/<int:pk>/', views.s_confirmed_project_detail, name='s_confirmed_project_detail'),
    path('s_admins/', views.s_admins, name='s_admins'),
    path('s_equipment/', views.s_equipment, name='s_equipment'),
    path('u_create_project/', views.u_create_project, name='u_create_project'),
    path('u_project_detail/<int:pk>/', views.u_project_detail, name='u_project_detail'),
    path('c_m1/<int:pk>/', views.c_m1, name='c_m1'),
    path('c_m2/<int:pk>/', views.c_m2, name='c_m2'),
    path('c_m3/<int:pk>/', views.c_m3, name='c_m3'),
    path('u_confirmed_project_detail/<int:pk>/', views.u_confirmed_project_detail, name='u_confirmed_project_detail')
]