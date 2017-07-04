from .models import Property
from django import forms
from django.utils.translation import gettext as _
#from taggit.forms import TagWidget

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('name', 'address', 'room_type',
             'size', 'property_type', 'price',
             'email', 'phone', 'features')
        widgets = {
            'room_type': forms.RadioSelect,
            'property_type': forms.RadioSelect,
        }