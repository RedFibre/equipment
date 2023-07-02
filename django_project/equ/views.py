from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Project, Lab,Equipment,TimeSlot,UserLab
from .forms import ProjectForm,EquipmentAssignmentForm
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
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            Project = form.save(commit=False)
            Project.user = request.user
            Project.lab = request.user.userlab.lab
            form.save()
            return redirect('u_projects')
    else:
        form = ProjectForm()
    
    labs = Lab.objects.all()
    context = {'form': form, }
    return render(request, 'equ/u_create_project.html', context)

#EDIT PROJECT
from datetime import datetime
from django.shortcuts import redirect

def u_project_detail(request, pk):
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

            return redirect('u_project_detail', pk=pk)
    else:
        form = EquipmentAssignmentForm(available_equipment)

    context = {
        'project': project,
        'available_equipment': available_equipment,
        'equipment_in_use': equipment_in_use,
        'booked_slots': booked_slots,
        'form': form
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




