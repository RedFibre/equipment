from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Project, Lab,Equipment,Booking,UserLab
from .forms import ProjectForm,BookingFormSet
from datetime import datetime,timedelta,timezone
from django.views import View


def user_redirect(request):
    if request.user.groups.filter(name='admin').exists():
        return redirect('a_overview')
    elif request.user.groups.filter(name='labuser').exists():
        return redirect('u_projects')
    elif request.user.groups.filter(name='superadmin').exists():
        return redirect('s_overview')
    else:
        return redirect('login')
    
def superadmin_required(function):
    decorator = user_passes_test(lambda user: user.groups.filter(name='superadmin').exists())
    return decorator(function)

def admin_required(function):
    decorator = user_passes_test(lambda user: user.groups.filter(name='admin').exists())
    return decorator(function)

#SUPERADMIN VIEWS


@login_required
@superadmin_required
def s_overview(request):
    return render(request, 'equ/s_overview.html')

@login_required
@superadmin_required
def s_labs(request):
    return render(request, 'equ/s_labs.html')

@login_required
@superadmin_required
def s_admins(request):
    return render(request, 'equ/s_admins.html')

@login_required
@superadmin_required
def s_projects(request):
    return render(request, 'equ/s_projects.html')

@login_required
@superadmin_required
def s_equipment(request):
    return render(request, 'equ/s_equipment.html')

#ADMIN VIEWS

@login_required
@admin_required
def a_overview(request):
    return render(request, 'equ/a_overview.html')

@login_required
@admin_required
def a_members(request):  
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'equ/a_members.html',context)

@login_required
@admin_required
def a_equipment(request):
    return render(request, 'equ/a_equipment.html')

@login_required
@admin_required
def a_activity(request):
    return render(request, 'equ/a_activity.html')

#USER VIEWS

def labuser_required(function):
    decorator = user_passes_test(lambda user: user.groups.filter(name='labuser').exists())
    return decorator(function)


@login_required
@labuser_required
def u_projects(request):
    user_projects = Project.objects.filter(user=request.user)
    context = {'user_projects': user_projects}
    return render(request, 'equ/u_projects.html', context)


@login_required
@labuser_required
def u_help(request):
    return render(request, 'equ/u_help.html')

@login_required
@labuser_required
def u_settings(request):
    return render(request, 'equ/u_settings.html')


#PROJECT CREATION
def u_create_project(request):
    current_lab = request.user.userlab.lab
    available_equipment = Equipment.objects.filter(lab=current_lab)
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        booking_formset = BookingFormSet(request.POST, form_kwargs={'available_equipment': available_equipment})
        if project_form.is_valid() and booking_formset.is_valid():
            project = project_form.save(commit=False)
            project.user = request.user
            project.lab = current_lab
            project.save()
            for form, data in zip(booking_formset.forms, booking_formset.cleaned_data):
                print(form)
                booking = form.save(commit=False)
                booking.project = project
                booking.equipment = data.get('equipment')
                booking.start_time = data.get('start_time')
                booking.end_time = data.get('end_time')
                booking.materials = data.get('materials')
                print(booking)
                booking.save()
            return redirect('u_projects')
    else:
        project_form = ProjectForm()
        booking_formset = BookingFormSet(form_kwargs={'available_equipment': available_equipment})

    return render(request, 'equ/u_create_project.html', {'project_form': project_form, 'booking_formset': booking_formset})


#EDIT PROJECT
from datetime import datetime
from django.shortcuts import redirect

def u_project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    bookings = Booking.objects.filter(project=project)

    context = {
        'project': project,
        'bookings':bookings
    }
    return render(request, 'equ/u_project_detail.html', context)

#CALENDAR VIEWS

@login_required
def c_list(request):
    lab = request.user.userlab.lab
    print(lab)
    equipment_of_lab = Equipment.objects.filter(lab=lab)
    context = {'my_lab': lab, 'equipments':equipment_of_lab}
    return render(request, 'equ/c_list.html', context)

@login_required
def c_calendar(request, pk):
    lab = request.user.userlab.lab
    equipment = get_object_or_404(Equipment, pk=pk)
    context = {'equipment':equipment}
    return render(request, 'equ/c_calendar.html', context)




