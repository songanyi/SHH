from .models import Property
from django import forms
from taggit.forms import TagWidget

class PropertyForm(forms.ModelForm):
    
    class Meta:
        model = Property
        fields = ('address', 'size', 'email', 'phone', 'tags')
        widgets = {
            'tags': TagWidget()
        }