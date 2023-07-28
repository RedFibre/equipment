from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Project, Lab,Equipment,Booking,Material,Confirmed_Project,Confirmed_Booking,Archived_Booking,Archived_Project,Notification
from .forms import ProjectForm,BookingFormSet
from datetime import datetime,timedelta
from django.utils.timezone import localdate
import calendar
from django.core.exceptions import ValidationError


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
    labs = Lab.objects.all()
    context = {'labs' : labs}
    return render(request, 'equ/s_labs.html',context)

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
    user = request.user  
    lab = Lab.objects.get(lab_admin=user)
    users = User.objects.filter(userlab__lab=lab)
    context = {'users': users}
    return render(request, 'equ/a_members.html',context)

@login_required
@admin_required
def a_member_detail(request,pk):
    user = get_object_or_404(User,pk=pk)
    projects = Confirmed_Project.objects.filter(user=user)
    context = {'user': user, 'projects':projects}
    return render(request, 'equ/a_member_detail.html',context)

@login_required
@admin_required
def a_equipment(request):
    user = request.user  
    lab = Lab.objects.get(lab_admin=user)
    equipment = Equipment.objects.filter(lab=lab)
    equipment = equipment.prefetch_related('material_set')
    context = {'equipments':equipment}
    return render(request, 'equ/a_equipment.html',context)

@login_required
@admin_required
def a_activity(request):
    user = request.user
    lab = Lab.objects.get(lab_admin=user)
    print(lab)
    all_projects = Project.objects.filter(lab=lab)
    print(all_projects)
    context = {'all_projects': all_projects}
    return render(request, 'equ/a_activity.html', context)

@login_required
@admin_required
def a_project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    bookings = Booking.objects.filter(project=project)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            confirmed = Confirmed_Project.objects.create(
            name=project.name,
            description=project.description,
            lab=project.lab,
            user=project.user,
            start_date=project.start_date,
            end_date=project.end_date
        )
            for booking in bookings:
                confirmed_booking = Confirmed_Booking.objects.create(
                    project = confirmed,
                    equipment=booking.equipment,
                    start_time=booking.start_time,
                    end_time=booking.end_time)
                confirmed_booking.materials.set(booking.materials.all())
            Notification.objects.create(user=project.user,message=f"Your Request for Project {project.name} has been Accepted",timestamp=datetime.now())
            project.delete()
            return redirect('a_activity')

        elif action == 'reject':
            Notification.objects.create(user=project.user,message=f"Your Request for Project {project.name} has been Rejected",timestamp=datetime.now())
            # Delete the project
            project.delete()

            # Redirect to a success page or perform any other action
            return redirect('a_activity')

    context = {
        'project': project,
        'bookings': bookings
    }
    return render(request, 'equ/a_project_detail.html', context)
#USER VIEWS

def labuser_required(function):
    decorator = user_passes_test(lambda user: user.groups.filter(name='labuser').exists())
    return decorator(function)


@login_required
@labuser_required
def u_projects(request):
    user_projects = Project.objects.filter(user=request.user)
    user_confirmed_projects = Confirmed_Project.objects.filter(user=request.user)
    user_notifications = Notification.objects.filter(user=request.user)
    context = {'user_projects': user_projects, 'user_confirmed_projects':user_confirmed_projects, 'user_notifications': user_notifications}
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
    available_materials = Material.objects.filter(equipment__lab=current_lab)
    if request.method == 'POST':
        print(request.POST)
        project_form = ProjectForm(request.POST)
        booking_formset = BookingFormSet(request.POST, form_kwargs={'available_equipment': available_equipment, 'available_materials': available_materials})
        if project_form.is_valid() and booking_formset.is_valid():
            project = project_form.save(commit=False)
            project.user = request.user
            project.lab = current_lab
            project.save()
            for form, data in zip(booking_formset.forms, booking_formset.cleaned_data):
                booking = form.save(commit=False)
                booking.project = project
                booking.equipment = data.get('equipment')
                booking.start_time = data.get('start_time')
                booking.end_time = data.get('end_time')
                  # Check for overlapping bookings
                overlapping_bookings = Confirmed_Booking.objects.filter(
                    equipment=booking.equipment,
                    start_time__lt=booking.end_time,
                    end_time__gt=booking.start_time,
                )
                if overlapping_bookings.exists():
                    error_message = "You Booked a slot that was already booked. Please check the calendar."
                    project.delete()
                    return render(request, 'equ/u_create_project.html', {'project_form': project_form, 'booking_formset': booking_formset, 'error_message': error_message})
                booking.save()
                materials = data.get('materials')
                booking.materials.set(materials)              
            return redirect('u_projects')
    
    else:
        project_form = ProjectForm()
        booking_formset = BookingFormSet(form_kwargs={'available_equipment': available_equipment, 'available_materials': available_materials})

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

def u_confirmed_project_detail(request, pk):
    confirmed_project = get_object_or_404(Confirmed_Project, pk=pk)
    confirmed_bookings = Confirmed_Booking.objects.filter(project=confirmed_project)

    context = {
        'project': confirmed_project,
        'bookings':confirmed_bookings
    }
    if request.method == 'POST':
        archived_project = Archived_Project.objects.create(
            name=confirmed_project.name,
            description=confirmed_project.description,
            lab=confirmed_project.lab,
            user=confirmed_project.user,
            start_date=confirmed_project.start_date,
            end_date=confirmed_project.end_date
        )
        for booking in confirmed_bookings:
            archived_booking = Archived_Booking.objects.create(
                project=archived_project,
                equipment=booking.equipment,
                start_time=booking.start_time,
                end_time=booking.end_time
            )
            archived_booking.materials.set(booking.materials.all())

        confirmed_project.delete()
        return redirect('u_projects')


    return render(request, 'equ/u_confirmed_project_detail.html', context)

#CALENDAR VIEWS

@login_required
def c_list(request):
    lab = request.user.userlab.lab
    equipment_of_lab = Equipment.objects.filter(lab=lab)

    current_date = datetime.today()
    months_names = []
    current_month_name = current_date.strftime("%B")
    months_names.append(current_month_name)
    for i in range(1, 3):
        next_month = current_date.replace(month=current_date.month + i)
        next_month_name = next_month.strftime("%B")
        months_names.append(next_month_name)


    context = {'my_lab': lab, 'equipments':equipment_of_lab,'months':months_names}
    return render(request, 'equ/c_list.html', context)

@login_required
def c_m1(request, pk):
    lab = request.user.userlab.lab
    equipment = get_object_or_404(Equipment, pk=pk)
    bookings = Confirmed_Booking.objects.filter(equipment=equipment)

    # Calculate date range for the current month
    today = localdate()  # Use localdate() to get the current date without time
    _, last_day_of_month = calendar.monthrange(today.year, today.month)
    date_range = [today + timedelta(days=i) for i in range(last_day_of_month - today.day + 1)]

    # Prepare time slots from 10 AM to 6 PM
    start_time = datetime(today.year, today.month, today.day, 10)
    time_slots = [start_time + timedelta(hours=i) for i in range(10)]
    time_slot_ranges = [(time_slots[i], time_slots[i + 1]) for i in range(len(time_slots) - 1)]

    context = {
        'equipment': equipment,
        'bookings': bookings,
        'date_range': date_range,
        'time_slots': time_slots,
        'time_slot_ranges': time_slot_ranges
    }

    return render(request, 'equ/c_m1.html', context)

@login_required
def c_m2(request, pk):
    lab = request.user.userlab.lab
    equipment = get_object_or_404(Equipment, pk=pk)
    bookings = Confirmed_Booking.objects.filter(equipment=equipment)

    # Calculate date range for the next month
    today = localdate()  # Use localdate() to get the current date without time
    _, last_day_of_month = calendar.monthrange(today.year, today.month)
    first_day_next_month = today.replace(day=1) + timedelta(days=last_day_of_month)
    _, last_day_next_month = calendar.monthrange(first_day_next_month.year, first_day_next_month.month)
    date_range = [first_day_next_month + timedelta(days=i) for i in range(last_day_next_month)]

    # Prepare time slots from 10 AM to 6 PM
    start_time = datetime(first_day_next_month.year, first_day_next_month.month, first_day_next_month.day, 10)
    time_slots = [start_time + timedelta(hours=i) for i in range(10)]
    time_slot_ranges = [(time_slots[i], time_slots[i + 1]) for i in range(len(time_slots) - 1)]

    context = {
        'equipment': equipment,
        'bookings': bookings,
        'date_range': date_range,
        'time_slots': time_slots,
        'time_slot_ranges': time_slot_ranges
    }

    return render(request, 'equ/c_m2.html', context)

@login_required
def c_m3(request, pk):
    lab = request.user.userlab.lab
    equipment = get_object_or_404(Equipment, pk=pk)
    bookings = Confirmed_Booking.objects.filter(equipment=equipment)

    # Calculate date range for the month after next
    today = localdate()  # Use localdate() to get the current date without time
    _, last_day_of_month = calendar.monthrange(today.year, today.month)
    first_day_next_month = today.replace(day=1) + timedelta(days=last_day_of_month)
    _, last_day_next_month = calendar.monthrange(first_day_next_month.year, first_day_next_month.month)
    first_day_month_after_next = first_day_next_month.replace(day=1) + timedelta(days=last_day_next_month)
    _, last_day_month_after_next = calendar.monthrange(first_day_month_after_next.year, first_day_month_after_next.month)
    date_range = [first_day_month_after_next + timedelta(days=i) for i in range(last_day_month_after_next)]

    # Prepare time slots from 10 AM to 6 PM
    start_time = datetime(first_day_month_after_next.year, first_day_month_after_next.month, first_day_month_after_next.day, 10)
    time_slots = [start_time + timedelta(hours=i) for i in range(10)]
    time_slot_ranges = [(time_slots[i], time_slots[i + 1]) for i in range(len(time_slots) - 1)]

    context = {
        'equipment': equipment,
        'bookings': bookings,
        'date_range': date_range,
        'time_slots': time_slots,
        'time_slot_ranges': time_slot_ranges
    }

    return render(request, 'equ/c_m3.html', context)


