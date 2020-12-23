from django import forms
from .models import mesurementsofdistance
 
class MeasurementsForm(forms.ModelForm):
    class Meta:
        model = mesurementsofdistance
        fields = ('destination',)
        