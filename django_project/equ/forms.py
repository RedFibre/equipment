from django import forms
from .models import Project, Booking,Material
from django.forms import formset_factory,DateTimeInput, DateInput
from datetime import datetime

class CustomDateTimeInput(DateTimeInput):
    def format_value(self, value):
        y = value.year
        m = value.month
        d = value.day
        h = value.hour
        new_value = datetime(year=y, month=m, day=d, hour=h, minute=0, second=0)
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
    materials = forms.ModelMultipleChoiceField(queryset=Material.objects.none(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Booking
        fields = ['equipment','start_time', 'end_time', 'materials']
        widgets = {
            'equipment': forms.Select(choices=()),
            'start_time': CustomDateTimeInput(format='%d/%m/%Y %I:%M %p'),
            'end_time': CustomDateTimeInput(format='%d/%m/%Y %I:%M %p')
        }

    def __init__(self, *args, **kwargs):
        available_equipment = kwargs.pop('available_equipment')
        available_materials = kwargs.pop('available_materials')
        super().__init__(*args, **kwargs)
        self.fields['equipment'].widget.choices = [(equipment.id, equipment.name) for equipment in available_equipment]
        self.fields['start_time'].widget = CustomDateTimeInput(attrs={'type': 'datetime-local','step': '3600'},format='%Y-%m-%d %H:%M')
        self.fields['end_time'].widget = CustomDateTimeInput(attrs={'type': 'datetime-local', 'step': '3600'},format='%Y-%m-%d %H:%M')
        self.fields['materials'].queryset = available_materials

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
