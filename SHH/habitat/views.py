from django.shortcuts import render
from django.http import HttpResponse
from django import forms

from .models import Property
from .models import Contact
from .models import Images
from .forms import PropertyForm

# Create your views here.
def index(request):
    context = {
        'listImages':[
            {'url': 'images/listing/list1.png', 'name': 'apartment 1'},
            {'url': 'images/listing/list2.png', 'name': 'apartment 2'},
            {'url': 'images/listing/list3.png', 'name': 'apartment 3'},
        ]

    }
    return render(request, 'index.html', context)

def search(request):
    context = {}
    return render(request, 'search.html', context)

def work_details(request):
    context = {}
    return render(request, 'work-details.html', context)

def renter_guide(request):
    context = {}
    return render(request, 'renter-guide.html', context)

def view_property(request):
    properties = Property.objects.order_by('-pub_date')[:10]
    context = {
        'property_list' : properties,
    }

    return render(request, 'view-property.html', context)


def add_property(request):
    
    if request.method == 'POST':
        form = PropertyForm(request.POST)    
        if form.is_valid():
            address = form.cleaned_data['address']
            size = form.cleaned_data['size']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            tags = form.cleaned_data['tags']

            prop = Property.objects.create(address=address, size=size, email=email, phone=phone)
            '''
            prop.size = size
            prop.email = email
            prop.phone = phone
            prop.pub_date = now
            '''
            prop.tags.add(*tags)
            prop.save()

            return HttpResponse('/settings/')
    else:
        form = PropertyForm()

    return render(request, 'add-property.html', {'form': form})