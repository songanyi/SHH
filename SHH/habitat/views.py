from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Property
from .models import Contact
from .models import Images
from .forms import PropertyForm

PAGESIZE = 5
ADJ_PAGES = 2

# reference getApartments
# url->id, img->load by foreign key, text1->address, text2->description.
def getFeatures():
    return [
            {'img': 'images/listing/list1.png', 'text': 'apartment 1', 'url': '/work-details/1'},
            {'img': 'images/listing/list2.png', 'text': 'apartment 2', 'url': '/work-details/2'},
            {'img': 'images/listing/list3.png', 'text': 'apartment 3', 'url': '/work-details/3'},
        ]

# can be saved in DB
def getRenterGuides():
    return [
            {'url': '/renter-guide/', 'text': 'guide 1'},
            {'url': '/renter-guide/', 'text': 'guide 2'},
            {'url': '/renter-guide/', 'text': 'guide 3'},
            {'url': '/renter-guide/', 'text': 'guide 4'},
            {'url': '/renter-guide/', 'text': 'guide 5'},
        ]

# can be saved in DB    
def getPlatforms():
    return [
            {'url': '#', 'text': 'platform 1'},
            {'url': '#', 'text': 'platform 2'},
            {'url': '#', 'text': 'platform 3'},
        ]

# can be saved in DB
def getPortfolios():
    return [
            {'img': 'images/portfolio/work-1.jpg', 'text1': 'The Shape of Design', 'text2': 'Branding/Graphic', 'url': 'work-details/1'},
            {'img': 'images/portfolio/work-2.jpg', 'text1': 'czarna kawka', 'text2': 'Branding', 'url': '/work-details/2'},
            {'img': 'images/portfolio/work-3.jpg', 'text1': 'czarna kawka', 'text2': 'Branding', 'url': '/work-details/3'},
            {'img': 'images/portfolio/work-4.jpg', 'text1': 'czarna kawka', 'text2': 'Branding', 'url': '/work-details/4'},
            {'img': 'images/portfolio/work-5.jpg', 'text1': 'czarna kawka', 'text2': 'Branding', 'url': '/work-details/5'},
            {'img': 'images/portfolio/work-6.jpg', 'text1': 'czarna kawka', 'text2': 'Branding', 'url': '/work-details/6'},
            {'img': 'images/portfolio/work-1.jpg', 'text1': 'The Shape of Design', 'text2': 'Branding/Graphic', 'url': '/work-details/1'},
            {'img': 'images/portfolio/work-2.jpg', 'text1': 'czarna kawka', 'text2': 'Branding', 'url': '/work-details/2'},
        ]

# can be saved in DB
def getTestimonials():
    return [
            {'text1':'"Integer posuere erat a ante venenatis dapibus posuere velit aliquet. Donec sed odio dui. Phasellus non dolor nibh. Nullam elementum Aenean eu leo quam..."', 'text2':'Rene Brown, Open Window production'},
            {'text1':'"Cras dictum tellus dui, vitae sollicitudin ipsum. Phasellus non dolor nibh. Nullam elementum tellus pretium feugiat shasellus non dolor nibh. Nullam elementum tellus pretium feugiat."', 'text2':'Brain Rice, Lexix Private Limited.'},
            {'text1':'"Cras mattis consectetur purus sit amet fermentum. Donec sed odio dui. Aenean lacinia bibendum nulla sed consectetur...."', 'text2':'Andi Simond, Global Corporate Inc'},
            {'text1':'"Lorem ipsum dolor sit amet, consectetur adipiscing elitPhasellus non dolor nibh. Nullam elementum tellus pretium feugiat. Cras dictum tellus dui sollcitudin."', 'text2':'Kristy Gabbor, Martix Media'},
        ]

# can be saved in DB
def getRenterGuideImg():
    return 'images/guide/guide1.jpg'

# can be saved in DB
def getNeighborhoods():
    return [
        {'area': 'French Concession', 'img': 'images/portfolio/work-2.jpg', 'class': 'cur', 'text': 'The French Concession, the former French colonial possession, is today a charming, historic district known for its European architecture and tree-lined streets, as well as its shopping, bars and cafes. Most of the action centers on the main east-west thoroughfare, Huaihai Road, an upscale shopping destination. You can also tour the area around Dongping Road, where dozens of the city\'s hottest bars are active nightly. Shopping in the area is a bit overpriced, but you\'ll find unique, one-of-a-kind items here that may be worth the money.'},
        {'area': 'Chang Ning', 'img': 'images/portfolio/work-2.jpg', 'class': '', 'text': 'Chang Ning, the former French colonial possession, is today a charming, historic district known for its European architecture and tree-lined streets, as well as its shopping, bars and cafes. Most of the action centers on the main east-west thoroughfare, Huaihai Road, an upscale shopping destination. You can also tour the area around Dongping Road, where dozens of the city\'s hottest bars are active nightly. Shopping in the area is a bit overpriced, but you\'ll find unique, one-of-a-kind items here that may be worth the money.'},
        {'area': 'Jing An', 'img': 'images/portfolio/work-2.jpg', 'class': '', 'text': 'Jing An, the former French colonial possession, is today a charming, historic district known for its European architecture and tree-lined streets, as well as its shopping, bars and cafes. Most of the action centers on the main east-west thoroughfare, Huaihai Road, an upscale shopping destination. You can also tour the area around Dongping Road, where dozens of the city\'s hottest bars are active nightly. Shopping in the area is a bit overpriced, but you\'ll find unique, one-of-a-kind items here that may be worth the money.'},
        {'area': 'Huang Pu', 'img': 'images/portfolio/work-2.jpg', 'class': '', 'text': 'Huang Pu, the former French colonial possession, is today a charming, historic district known for its European architecture and tree-lined streets, as well as its shopping, bars and cafes. Most of the action centers on the main east-west thoroughfare, Huaihai Road, an upscale shopping destination. You can also tour the area around Dongping Road, where dozens of the city\'s hottest bars are active nightly. Shopping in the area is a bit overpriced, but you\'ll find unique, one-of-a-kind items here that may be worth the money.'},
    ]


def getApartments():
    return [
        # url->id, img->load by foreign key, text1->address, text2->description.
        {'url': '/work-details/1', 'img': 'images/listing/list1.png', 'text1': 'Apartment 1', 'text2': 'paragraph 1', 'tags':[],},
        {'url': '/work-details/2', 'img': 'images/listing/list2.png', 'text1': 'Apartment 2', 'text2': 'paragraph 2', 'tags':[],},
        {'url': '/work-details/3', 'img': 'images/listing/list3.png', 'text1': 'Apartment 3', 'text2': 'paragraph 3', 'tags':[],},
        {'url': '/work-details/1', 'img': 'images/listing/list1.png', 'text1': 'Apartment 1', 'text2': 'paragraph 1', 'tags':[],},
        {'url': '/work-details/2', 'img': 'images/listing/list2.png', 'text1': 'Apartment 2', 'text2': 'paragraph 2', 'tags':[],},
        {'url': '/work-details/1', 'img': 'images/listing/list1.png', 'text1': 'Apartment 1', 'text2': 'paragraph 1', 'tags':[],},
        {'url': '/work-details/2', 'img': 'images/listing/list2.png', 'text1': 'Apartment 2', 'text2': 'paragraph 2', 'tags':[],},
        {'url': '/work-details/3', 'img': 'images/listing/list3.png', 'text1': 'Apartment 3', 'text2': 'paragraph 3', 'tags':[],},
        {'url': '/work-details/1', 'img': 'images/listing/list1.png', 'text1': 'Apartment 1', 'text2': 'paragraph 1', 'tags':[],},
        {'url': '/work-details/2', 'img': 'images/listing/list2.png', 'text1': 'Apartment 2', 'text2': 'paragraph 2', 'tags':[],},
        {'url': '/work-details/1', 'img': 'images/listing/list1.png', 'text1': 'Apartment 1', 'text2': 'paragraph 1', 'tags':[],},
        {'url': '/work-details/2', 'img': 'images/listing/list2.png', 'text1': 'Apartment 2', 'text2': 'paragraph 2', 'tags':[],},
        {'url': '/work-details/3', 'img': 'images/listing/list3.png', 'text1': 'Apartment 3', 'text2': 'paragraph 3', 'tags':[],},
        {'url': '/work-details/1', 'img': 'images/listing/list1.png', 'text1': 'Apartment 1', 'text2': 'paragraph 1', 'tags':[],},
        {'url': '/work-details/2', 'img': 'images/listing/list2.png', 'text1': 'Apartment 2', 'text2': 'paragraph 2', 'tags':[],},
        {'url': '/work-details/1', 'img': 'images/listing/list1.png', 'text1': 'Apartment 1', 'text2': 'paragraph 1', 'tags':[],},
        {'url': '/work-details/2', 'img': 'images/listing/list2.png', 'text1': 'Apartment 2', 'text2': 'paragraph 2', 'tags':[],},
        {'url': '/work-details/3', 'img': 'images/listing/list3.png', 'text1': 'Apartment 3', 'text2': 'paragraph 3', 'tags':[],},
        {'url': '/work-details/1', 'img': 'images/listing/list1.png', 'text1': 'Apartment 1', 'text2': 'paragraph 1', 'tags':[],},
        {'url': '/work-details/2', 'img': 'images/listing/list2.png', 'text1': 'Apartment 2', 'text2': 'paragraph 2', 'tags':[],},
        {'url': '/work-details/1', 'img': 'images/listing/list1.png', 'text1': 'Apartment 1', 'text2': 'paragraph 1', 'tags':[],},
        {'url': '/work-details/2', 'img': 'images/listing/list2.png', 'text1': 'Apartment 2', 'text2': 'paragraph 2', 'tags':[],},
        {'url': '/work-details/3', 'img': 'images/listing/list3.png', 'text1': 'Apartment 3', 'text2': 'paragraph 3', 'tags':[],},
        {'url': '/work-details/1', 'img': 'images/listing/list1.png', 'text1': 'Apartment 1', 'text2': 'paragraph 1', 'tags':[],},
        {'url': '/work-details/2', 'img': 'images/listing/list2.png', 'text1': 'Apartment 2', 'text2': 'paragraph 2', 'tags':[],},
    ]


def getPagedApartments(page):
    apartments = getApartments()
    paginator = Paginator(apartments, PAGESIZE)
    try:
        apartments = paginator.page(page)
    except PageNotAnInteger:
        apartments = paginator.page(1)
    except EmptyPage:
        apartments = paginator.page(paginator.num_pages)
    


    #https://djangosnippets.org/snippets/73/
    page_numbers = [n for n in \
                    range(apartments.number - ADJ_PAGES, apartments.number + ADJ_PAGES + 1) \
                    if n > 0 and n <= paginator.num_pages]

    return {
        'data': apartments, 
        'page_numbers': page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
    }


def getAptDetails(id):
    return {
        'apt_name': 'apt_name',
        'descriptions': ['Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Maecenas', 
                    'ut fermentum massa justo sit amet risus. Maecenas sed diam eget risus varius blandit sit amet non magna. Nullam quis',
                    'risus eget urna mollis ornare vel eu leo.',],
        'contact_url': '/people/?id=1',
        'tags': [],
        # Image
        'apt_imgs': [
            {'img': 'images/slider/slid1.jpg', 'alt': 'First slide', 'class': 'active', "idx": "0"},
            {'img': 'images/slider/slid2.jpg', 'alt': 'Second slide', 'class': '', "idx": "1"},
            {'img': 'images/slider/slid3.jpg', 'alt': 'Third slide', 'class': '', "idx": "2"},
        ],
        # Comment
        'testimonials': [
            {'text1':'"Integer posuere erat a ante venenatis dapibus posuere velit aliquet. Donec sed odio dui. Phasellus non dolor nibh. Nullam elementum Aenean eu leo quam..."', 'text2':'Rene Brown, Open Window production'},
            {'text1':'"Cras dictum tellus dui, vitae sollicitudin ipsum. Phasellus non dolor nibh. Nullam elementum tellus pretium feugiat shasellus non dolor nibh. Nullam elementum tellus pretium feugiat."', 'text2':'Brain Rice, Lexix Private Limited.'},
            {'text1':'"Cras mattis consectetur purus sit amet fermentum. Donec sed odio dui. Aenean lacinia bibendum nulla sed consectetur...."', 'text2':'Andi Simond, Global Corporate Inc'},
            {'text1':'"Lorem ipsum dolor sit amet, consectetur adipiscing elitPhasellus non dolor nibh. Nullam elementum tellus pretium feugiat. Cras dictum tellus dui sollcitudin."', 'text2':'Kristy Gabbor, Martix Media'},
        ]
    }

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


def work_details(request):
    context = getAptDetails(0)
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