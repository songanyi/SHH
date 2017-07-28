from .models import Property, UserProfile, User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
#from taggit.forms import TagWidget


class PropertyForm(forms.ModelForm):
    '''
    https://stackoverflow.com/questions/15846120/uploading-a-file-in-django-with-modelforms
    https://stackoverflow.com/questions/32889199/how-to-upload-multiple-images-using-modelformset-django
    '''
    class Meta:
        model = Property
        fields = ['name', 'address', 'room_type',
                  'size', 'property_type', 'price',
                  'email', 'phone', 'features']
        widgets = {
            'room_type': forms.RadioSelect,
            'property_type': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['size'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    #https://stackoverflow.com/questions/5827590/css-styling-in-django-forms
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat Password'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'phonenumber', 'email']


class PropertySearchForm(forms.ModelForm):
    '''
    https://stackoverflow.com/questions/15846120/uploading-a-file-in-django-with-modelforms
    https://stackoverflow.com/questions/32889199/how-to-upload-multiple-images-using-modelformset-django
    '''
    price_low = forms.IntegerField('Price Range High')
    price_high = forms.IntegerField('Price Range Low')
    min_size = forms.IntegerField('Minimum Room Size')

    class Meta:
        model = Property
        fields = ['address', 'room_type', 'price_low', 'price_high',
                  'min_size', 'property_type',
                  'features',
                  ]
        widgets = {
            'room_type': forms.RadioSelect,
            'property_type': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super(PropertySearchForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['min_size'].widget.attrs['class'] = 'form-control'
        self.fields['price_low'].widget.attrs['class'] = 'form-control'
        self.fields['price_high'].widget.attrs['class'] = 'form-control'