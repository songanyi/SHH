# encoding: utf-8
from django.conf.urls import url
from habitat.views import (PictureListView, PictureDeleteView, AngularVersionCreateView,
                            PictureCreateView)

urlpatterns = [
    url(r'^angular/$', AngularVersionCreateView.as_view(), name='upload-angular'),
    url(r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), name='upload-delete'),
    #url(r'^view/$', PictureListView.as_view(), name='upload-view'),
    url(r'^view/(?P<pid>\d+)$', PictureListView.as_view(), name='upload-view'),
]