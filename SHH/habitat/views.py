from django.shortcuts import render
from django.http import HttpResponse

from .models import Contact
from .models import Property
from .models import Images

# Create your views here.
def index(request):
    return HttpResponse("Hello world")


def view_property(request):
    properties = Property.objects.order_by('-pub_date')[:10]
    context = {
        'property_list' : properties,
    }

    return render(request, 'view-property.html', context)
