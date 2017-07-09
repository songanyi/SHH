# encoding: utf-8
import os
import json

from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.template.context_processors import csrf
from django.urls import reverse
from django.views import generic
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, ListView

from .models import Property
from .models import Contact
from .models import Images
from .forms import PropertyForm
from .response import JSONResponse, response_mimetype
from .serialize import *

PAGESIZE = 5
ADJ_PAGES = 2

# reference getApartments
# url->id, img->load by foreign key, text1->address, text2->description.

def getFeatures():
    return [
        {'img': '/static/images/listing/list1.png',
            'name': 'apartment 1', 'id': '1'},
        {'img': '/static/images/listing/list2.png',
                'name': 'apartment 2', 'id': '2'},
        {'img': '/static/images/listing/list3.png',
                'name': 'apartment 3', 'id': '3'},
    ]

# can be saved in DB


def getRenterGuides():
    return [
        {'url': '/renter-guide/', 'text': 'Find Your Style'},
        {'url': '/renter-guide/', 'text': 'Explore Neighborhood'},
        {'url': '/renter-guide/', 'text': 'Fee vs No-Fee'},
        {'url': '/renter-guide/', 'text': 'Signing and Deposits'},
        {'url': '/renter-guide/', 'text': 'Bait and Switch'},
    ]

# can be saved in DB


def getPlatforms():
    return [
        {'url': '#', 'text': 'Facebook'},
        {'url': '#', 'text': 'Twitter'},
        {'url': '#', 'text': 'Weibo'},
        {'url': '#', 'text': 'Slack Group'},
    ]

# can be saved in DB


def getPortfolios():
    return [
        {'img': '/static/images/portfolio/work-1.jpg', 'text1': 'The Shape of Design',
            'text2': 'Branding/Graphic', 'url': 'work-details/1'},
        {'img': '/static/images/portfolio/work-2.jpg', 'text1': 'czarna kawka',
                'text2': 'Branding', 'url': '/work-details/2'},
        {'img': '/static/images/portfolio/work-3.jpg', 'text1': 'czarna kawka',
                'text2': 'Branding', 'url': '/work-details/3'},
        {'img': '/static/images/portfolio/work-4.jpg', 'text1': 'czarna kawka',
                'text2': 'Branding', 'url': '/work-details/4'},
        {'img': '/static/images/portfolio/work-5.jpg', 'text1': 'czarna kawka',
                'text2': 'Branding', 'url': '/work-details/5'},
        {'img': '/static/images/portfolio/work-6.jpg', 'text1': 'czarna kawka',
                'text2': 'Branding', 'url': '/work-details/6'},
        {'img': '/static/images/portfolio/work-1.jpg', 'text1': 'The Shape of Design',
                'text2': 'Branding/Graphic', 'url': '/work-details/1'},
        {'img': '/static/images/portfolio/work-2.jpg', 'text1': 'czarna kawka',
                'text2': 'Branding', 'url': '/work-details/2'},
    ]

# can be saved in DB


def getTestimonials():
    return [
        {'text1': '"Integer posuere erat a ante venenatis dapibus posuere velit aliquet. Donec sed odio dui. Phasellus non dolor nibh. Nullam elementum Aenean eu leo quam..."',
            'text2': 'Rene Brown, Open Window production'},
        {'text1': '"Cras dictum tellus dui, vitae sollicitudin ipsum. Phasellus non dolor nibh. Nullam elementum tellus pretium feugiat shasellus non dolor nibh. Nullam elementum tellus pretium feugiat."',
         'text2': 'Brain Rice, Lexix Private Limited.'},
        {'text1': '"Cras mattis consectetur purus sit amet fermentum. Donec sed odio dui. Aenean lacinia bibendum nulla sed consectetur...."',
         'text2': 'Andi Simond, Global Corporate Inc'},
        {'text1': '"Lorem ipsum dolor sit amet, consectetur adipiscing elitPhasellus non dolor nibh. Nullam elementum tellus pretium feugiat. Cras dictum tellus dui sollcitudin."',
         'text2': 'Kristy Gabbor, Martix Media'},
    ]

# can be saved in DB


def getRenterGuideImg():
    return 'images/guide/guide1.jpg'


# TODO can be saved in DB
# Obsolete
def getNeighborhoods():
    return [
        {'area': 'French Concession', 'img': '/static/images/portfolio/work-2.jpg', 'class': 'cur', 'text': 'The French Concession, the former French colonial possession, is today a charming, historic district known for its European architecture and tree-lined streets, as well as its shopping, bars and cafes. Most of the action centers on the main east-west thoroughfare, Huaihai Road, an upscale shopping destination. You can also tour the area around Dongping Road, where dozens of the city\'s hottest bars are active nightly. Shopping in the area is a bit overpriced, but you\'ll find unique, one-of-a-kind items here that may be worth the money.'},
        {'area': 'Chang Ning', 'img': '/static/images/portfolio/work-2.jpg', 'class': '', 'text': 'Chang Ning, the former French colonial possession, is today a charming, historic district known for its European architecture and tree-lined streets, as well as its shopping, bars and cafes. Most of the action centers on the main east-west thoroughfare, Huaihai Road, an upscale shopping destination. You can also tour the area around Dongping Road, where dozens of the city\'s hottest bars are active nightly. Shopping in the area is a bit overpriced, but you\'ll find unique, one-of-a-kind items here that may be worth the money.'},
        {'area': 'Jing An', 'img': '/static/images/portfolio/work-2.jpg', 'class': '', 'text': 'Jing An, the former French colonial possession, is today a charming, historic district known for its European architecture and tree-lined streets, as well as its shopping, bars and cafes. Most of the action centers on the main east-west thoroughfare, Huaihai Road, an upscale shopping destination. You can also tour the area around Dongping Road, where dozens of the city\'s hottest bars are active nightly. Shopping in the area is a bit overpriced, but you\'ll find unique, one-of-a-kind items here that may be worth the money.'},
        {'area': 'Huang Pu', 'img': '/static/images/portfolio/work-2.jpg', 'class': '', 'text': 'Huang Pu, the former French colonial possession, is today a charming, historic district known for its European architecture and tree-lined streets, as well as its shopping, bars and cafes. Most of the action centers on the main east-west thoroughfare, Huaihai Road, an upscale shopping destination. You can also tour the area around Dongping Road, where dozens of the city\'s hottest bars are active nightly. Shopping in the area is a bit overpriced, but you\'ll find unique, one-of-a-kind items here that may be worth the money.'},
    ]


def getApartments():
    return Property.objects.all()


def getPagedApartments(page):
    apartments = getApartments()
    paginator = Paginator(apartments, PAGESIZE)
    try:
        apartments = paginator.page(page)
    except PageNotAnInteger:
        apartments = paginator.page(1)
    except EmptyPage:
        apartments = paginator.page(paginator.num_pages)

    # https://djangosnippets.org/snippets/73/
    page_numbers = [n for n in
                    range(apartments.number - ADJ_PAGES,
                          apartments.number + ADJ_PAGES + 1)
                    if n > 0 and n <= paginator.num_pages]

    return {
        'has_previous': apartments.has_previous,
        'has_next': apartments.has_next,
        'previous_page_number': apartments.previous_page_number,
        'num_pages': apartments.paginator.num_pages,
        'next_page_number': apartments.next_page_number,
        'number': apartments.number,
        'data': [serialize_search(p) for p in apartments],
        'page_numbers': page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
    }

# TODO


def getAptDetails(id):
    apt = get_object_or_404(Property, pk=id)
    images = Images.objects.filter(prop_id=id)
    if images is None or len(images) <= 0:
        images = ["/static/images/listing/list1.png", "/static/images/listing/list2.png", "/static/images/listing/list3.png"]
    
    content = {
        'apt_name': apt.name,
        'address': apt.address,

        'room_type': apt.room_type,
        'property_type': apt.property_type,
        'price': apt.price,
        # TODO merge room_type, property_type, price into descriptions
        'descriptions': ['Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Maecenas',
                         'ut fermentum massa justo sit amet risus. Maecenas sed diam eget risus varius blandit sit amet non magna. Nullam quis',
                         'risus eget urna mollis ornare vel eu leo.', ],
        #'contact_url': '/people/?uid={0}'.format(apt.user.id),
        'contact_url': 'mailto:{0}'.format(apt.email),
        'pub_date': apt.pub_date,
        'tags': apt.get_features_list(),
        # Image
        'apt_imgs': [serialize_work_details(c, image) for c, image in enumerate(images)],
        # Comment
        # TODO add related comments or use commment services
        'testimonials': [
            {'text1': '"Integer posuere erat a ante venenatis dapibus posuere velit aliquet. Donec sed odio dui. Phasellus non dolor nibh. Nullam elementum Aenean eu leo quam..."',
                'text2': 'Rene Brown, Open Window production'},
            {'text1': '"Cras dictum tellus dui, vitae sollicitudin ipsum. Phasellus non dolor nibh. Nullam elementum tellus pretium feugiat shasellus non dolor nibh. Nullam elementum tellus pretium feugiat."',
                'text2': 'Brain Rice, Lexix Private Limited.'},
            {'text1': '"Cras mattis consectetur purus sit amet fermentum. Donec sed odio dui. Aenean lacinia bibendum nulla sed consectetur...."',
                'text2': 'Andi Simond, Global Corporate Inc'},
            {'text1': '"Lorem ipsum dolor sit amet, consectetur adipiscing elitPhasellus non dolor nibh. Nullam elementum tellus pretium feugiat. Cras dictum tellus dui sollcitudin."',
                'text2': 'Kristy Gabbor, Martix Media'},
        ]
    }
    # print(content)
    return content

# ----------------------------------
# # Create your views here.
# ----------------------------------


def index(request):
    context = {
        'features': getFeatures(),
        'renterGuides': getRenterGuides(),
        'platforms': getPlatforms(),
        'portfolios': getPortfolios(),
        'testimonials': getTestimonials(),
    }
    return render(request, 'index.html', context)


def search(request, page):
    context = {
        'apartments': getPagedApartments(page),
    }
    return render(request, 'search.html', context)


def searchGet(request):
    page = request.GET.get('page')
    context = {
        'apartments': getPagedApartments(page),
    }
    return render(request, 'search.html', context)


def work_details(request, pid):
    context = getAptDetails(pid)
    return render(request, 'work-details.html', context)


def contact(request):
    context = {

    }
    return render(request, 'contact.html', context)


def renter_guide(request):
    context = {
        'bgImg': getRenterGuideImg(),
        'neighhorhoods': getNeighborhoods(),
    }
    return render(request, 'renter-guide.html', context)


def view_property(request):
    properties = Property.objects.order_by('-pub_date')[:10]
    context = {
        'property_list': properties,
    }

    return render(request, 'view-property.html', context)


#@login_required(login_url='/accounts/login/')
def upload_image_get(request):
    # return render(request, 'habitat/images_basicplus_form.html', {})
    return render(request, 'habitat/images_angular_form.html', {'pid': request.GET.get('pid')})


#@login_required(login_url='/accounts/login/')
def upload_image(request, pid):
    # return render(request, 'habitat/images_basicplus_form.html', {})
    # check pid and user
    return render(request, 'habitat/images_angular_form.html', {'pid': pid})


#@login_required(login_url='/accounts/login/')
def add_image(request, pid):
    return render(request, 'add-image.html', {'pid': pid})


#@login_required(login_url='/accounts/login/')
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        # print(form)
        print(form.is_valid())
        if form.is_valid():
            prop = form.save()
            return HttpResponseRedirect(reverse('add-image', args=(prop.id,)))

        else:
            data = json.dumps(form.errors)
            print("error:")
            print(data)
    else:
        form = PropertyForm()

    return render(request, 'add-property.html', {'form': form})


def login(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            return HttpResponseRedirect('/index/')

        username = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        stayloggedin = request.POST.get('stayloggedin')
        print(stayloggedin)
        if stayloggedin is None or stayloggedin == False:
            self.request.session.set_expiry(0)

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                if user.is_active:
                    auth.login(request, user)
                    data = {'success': True }
                else:
                    data = {'success': False, 'error': 'User is not active'}
            else:
                data = {'success': False, 'error': 'Wrong username and/or passowrd'}
                
            return HttpResponse(json.dumps(data), mimetypes='application/json')

        return HttpResponseBadRequest()
    else:
        return render(request, 'registration/login.html', {})


def logout(request):
    auth.logout(request)
    #TODO return to returnUrl
    return HttpResponseRedirect('/index/')


class PictureCreateView(CreateView):
    model = Images
    fields = "__all__"
    
    #@login_required(login_url='/accounts/login/')
    def form_valid(self, form):
        images = form.save(commit=False)
        #images.user = request.user
        images.save()
        form.save_m2m()

        self.object = images
        files = [serialize(self.object)]

        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        print(response)
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        print("error:")
        print(data)
        # handle unauthorized users
        return HttpResponse(content=data, status=400, content_type='application/json')


class AngularVersionCreateView(PictureCreateView):
    template_name_suffix = '_angular_form'


class PictureDeleteView(DeleteView):
    model = Images

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PictureListView(ListView):
    model = Images

    def render_to_response(self, context, **response_kwargs):
        pid = self.kwargs['pid']
        # print(self.get_queryset())
        files = [serialize(p) for p in self.get_queryset().filter(prop_id=pid)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
