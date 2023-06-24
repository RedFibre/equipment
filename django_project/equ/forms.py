from django import forms
from django.core.exceptions import ValidationError
from .models import Project, Equipment, TimeSlot

class EquipmentAssignmentForm(forms.Form):
    def __init__(self, available_equipment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['equipment'] = forms.ModelChoiceField(queryset=available_equipment, empty_label=None)

    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    def clean(self):
        cleaned_data = super().clean()
        equipment = cleaned_data.get('equipment')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if equipment and start_time and end_time:
            overlapping_slots = TimeSlot.objects.filter(equipment=equipment, start_time__lt=end_time, end_time__gt=start_time)
            if overlapping_slots.exists():
                raise ValidationError("This equipment is already booked for the selected time slot. Please Check The Calendar For Available Slots")

        return cleaned_data



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user']