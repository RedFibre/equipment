from django import forms
from django.core.exceptions import ValidationError
from .models import Project, Equipment, Booking,Material
from django.forms import inlineformset_factory,formset_factory




class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user','lab']


class BookingForm(forms.ModelForm):
    materials = forms.ModelMultipleChoiceField(queryset=Material.objects.none(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Booking
        fields = ['equipment','start_time', 'end_time', 'materials']
        widgets = {
            'equipment': forms.Select(choices=())
        }

    def __init__(self, *args, **kwargs):
        available_equipment = kwargs.pop('available_equipment')
        available_materials = kwargs.pop('available_materials')
        super().__init__(*args, **kwargs)
        self.fields['equipment'].widget.choices = [(equipment.id, equipment.name) for equipment in available_equipment]
        self.fields['materials'].queryset = available_materials
        
BookingFormSet = formset_factory(BookingForm, extra=1) 