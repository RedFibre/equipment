from django import forms
from django.core.exceptions import ValidationError
from .models import Project, Equipment, Booking
from django.forms import inlineformset_factory,formset_factory




class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user','lab']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['equipment','start_time', 'end_time', 'materials']
        widgets = {
            'equipment': forms.Select(choices=())
        }

    def __init__(self, *args, **kwargs):
        available_equipment = kwargs.pop('available_equipment')
        super().__init__(*args, **kwargs)
        self.fields['equipment'].widget.choices = [(equipment.id, equipment.name) for equipment in available_equipment]

BookingFormSet = formset_factory(BookingForm, extra=1) 