from django import forms
from .models import Project,Booking,Material,Profile,Equipment,Category
from django.forms import formset_factory,DateTimeInput, DateInput
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    pass

class CustomDateTimeInput(DateTimeInput):
    def format_value(self, value):
        if isinstance(value, datetime):
            y = value.year
            m = value.month
            d = value.day
            h = value.hour
            new_value = datetime(year=y, month=m, day=d, hour=h, minute=0, second=0)
        else:
            new_value = value
        return super().format_value(new_value)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user','lab']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['equipment','start_time', 'end_time']
        widgets = {
            'equipment': forms.Select(choices=()),
            'start_time': CustomDateTimeInput(format='%d/%m/%Y %I:%M %p'),
            'end_time': CustomDateTimeInput(format='%d/%m/%Y %I:%M %p')
        }

    def __init__(self, *args, **kwargs):
        available_equipment = kwargs.pop('available_equipment')
        super().__init__(*args, **kwargs)
        self.fields['equipment'].widget.choices = [(equipment.id, equipment.name) for equipment in available_equipment]
        self.fields['start_time'].widget = CustomDateTimeInput(attrs={'type': 'datetime-local','step': '3600'},format='%Y-%m-%d %H:%M')
        self.fields['end_time'].widget = CustomDateTimeInput(attrs={'type': 'datetime-local', 'step': '3600'},format='%Y-%m-%d %H:%M')
        


    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        # Custom validation for the format of start_time and end_time
        if start_time and start_time.minute != 0:
            self.add_error("start_time", "Booking should be in HH:00 Format")

        if end_time and end_time.minute != 0:
            self.add_error("end_time", "Booking should be in HH:00 Format")
        
        # Custom validation to check if start_time < end_time
        if start_time and end_time and start_time >= end_time:
             self.add_error("end_time", "End Time should be greater than Start Time")
        
        return cleaned_data
BookingFormSet = formset_factory(BookingForm, extra=1) 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'user_type',
            'lab',
            'first_name',
            'last_name',
            'contact_number',
            'email',
            'branch',
            'year_of_graduation',
            'institute_name',
            'training_record',
            'machines_trained_in',
            'how_heard_about',
        ]
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'branch': forms.TextInput(attrs={'class': 'form-control'}),
            'year_of_graduation': forms.NumberInput(attrs={'class': 'form-control'}),
            'institute_name': forms.TextInput(attrs={'class': 'form-control'}),
            'training_record': forms.Select(attrs={'class': 'form-control'}),
            'machines_trained_in': forms.TextInput(attrs={'class': 'form-control'}),
            'how_heard_about': forms.Select(attrs={'class': 'form-control'}),
        }

class EquipmentCreationForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'condition']

class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'stock']

class MaterialRequestForm(forms.Form):
    material_pk = forms.CharField(widget=forms.HiddenInput)
    request_type = forms.ChoiceField(choices=(('Borrow', 'Borrow'), ('Issue', 'Issue')))
    quantity = forms.IntegerField(min_value=1)
    

