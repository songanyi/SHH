"""SHH URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from habitat import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^view-property/', views.view_property, name='view-property'),
    url(r'^add-property/', views.add_property, name="add-property"),
    url(r'^renter-guide/', views.renter_guide, name="renter-guide"),
    url(r'^work-details/(?P<pid>\d+)', views.work_details, name="work-details"),
    url(r'^contact/', views.contact, name="contact"),
    url(r'^search/(?P<page>)\w{0,50}/', views.search, name="search"),
    url(r'^search/', views.searchGet, name="search-get"),
    url(r'^upload/', include('habitat.urls')),
    url(r'^upload-image/(?P<pid>\d+)', views.upload_image, name="upload-image"),
    url(r'^upload-image/', views.upload_image_get, name="upload-image-get"),

    url(r'^add-image/(?P<pid>\d+)', views.add_image, name="add-image"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:


'''
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('', 
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL, 'show_indexes': True}),
)
'''
#if settings.DEBUG:
#    from django.conf.urls.static import static
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)