from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Project, Lab,Equipment,TimeSlot
from .forms import ProjectForm,EquipmentAssignmentForm
from datetime import datetime,timedelta,timezone
from django.views import View


def user_redirect(request):
    if request.user.groups.filter(name='admin').exists():
        return redirect('home')
    elif request.user.groups.filter(name='labuser').exists():
        return redirect('calendaruser')
    elif request.user.groups.filter(name='superadmin').exists():
        return redirect('superoverview')
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
def superoverview(request):
    return render(request, 'equ/superoverview.html')

@login_required
@superadmin_required
def superlabs(request):
    return render(request, 'equ/superlabs.html')

@login_required
@superadmin_required
def superadmins(request):
    return render(request, 'equ/superadmins.html')

@login_required
@superadmin_required
def superprojects(request):
    return render(request, 'equ/superprojects.html')

@login_required
@superadmin_required
def superequipments(request):
    return render(request, 'equ/superequipments.html')

@login_required
@superadmin_required
def superinventory(request):
    return render(request, 'equ/superinventory.html')

#ADMIN VIEWS

@login_required
@admin_required
def home(request):
    return render(request, 'equ/home.html')

@login_required
@admin_required
def calendar(request):
    return render(request, 'equ/calendar.html')

@login_required
@admin_required
def members(request):  
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'equ/members.html',context)

@login_required
@admin_required
def equipment(request):
    return render(request, 'equ/equipment.html')

@login_required
@admin_required
def activity(request):
    return render(request, 'equ/activity.html')

@login_required
@admin_required
def inventory(request):
    return render(request, 'equ/inventory.html')


#USER VIEWS

def labuser_required(function):
    decorator = user_passes_test(lambda user: user.groups.filter(name='labuser').exists())
    return decorator(function)

@login_required
@labuser_required
def calendaruser(request):
    labs = Lab.objects.all()
    context = {'labs': labs}
    return render(request, 'equ/calendaruser.html', context)


@login_required
@labuser_required
def projects(request):
    user_projects = Project.objects.filter(user=request.user)
    context = {'user_projects': user_projects}
    return render(request, 'equ/projects.html', context)


@login_required
@labuser_required
def help(request):
    return render(request, 'equ/help.html')

@login_required
@labuser_required
def settings(request):
    return render(request, 'equ/settings.html')


#PROJECT CREATION
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            Project = form.save(commit=False)
            Project.user = request.user
            form.save()
            return redirect('create')
    else:
        form = ProjectForm()
    
    labs = Lab.objects.all()
    context = {'form': form, 'labs': labs}
    return render(request, 'equ/create_project.html', context)

#EDIT PROJECT
from datetime import datetime
from django.shortcuts import redirect

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    current_lab = project.lab
    available_equipment = Equipment.objects.filter(lab=current_lab)

    current_time = datetime.now()
 
    equipment_in_use = Equipment.objects.filter(timeslot__start_time__lt=current_time, timeslot__end_time__gt=current_time, lab=current_lab,project=project)

    booked_slots = TimeSlot.objects.filter(equipment__lab=current_lab, equipment__project=project).exclude(end_time__lt=current_time)

    if request.method == 'POST':
        form = EquipmentAssignmentForm(available_equipment, request.POST)
        if form.is_valid():
            equipment = form.cleaned_data['equipment']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']

            # Create a new time slot and assign the equipment
            time_slot = TimeSlot.objects.create(start_time=start_time, end_time=end_time, equipment=equipment)
            equipment.project = project
            equipment.usage = True
            equipment.save()

            return redirect('project_detail', pk=pk)
    else:
        form = EquipmentAssignmentForm(available_equipment)

    context = {
        'project': project,
        'available_equipment': available_equipment,
        'equipment_in_use': equipment_in_use,
        'booked_slots': booked_slots,
        'form': form
    }
    return render(request, 'equ/project_detail.html', context)

from django.utils import timezone

from django.utils import timezone

from django.utils import timezone

def format_timezone_offset(dt):
    offset = dt.utcoffset()
    offset_hours = offset.total_seconds() // 3600
    offset_minutes = (offset.total_seconds() % 3600) // 60
    offset_string = f"{int(offset_hours):+03d}:{int(offset_minutes):02d}"
    return offset_string

def labcalendar(request, pk):
    lab = Lab.objects.get(id=pk)
    equipments = lab.equipments.all()
    time_slots = TimeSlot.objects.filter(equipment__lab=lab)

    current_time = datetime.now()
    start_time = current_time.replace(minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=24)
    time_range = [start_time + timedelta(hours=i) for i in range(24)]

    context = {
        'lab': lab,
        'equipments': equipments,
        'time_range': time_range,
        'time_slots': time_slots,
    }

    return render(request, 'equ/labcalendar.html', context)






