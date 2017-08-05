# encoding: utf-8
import mimetypes
import re
from django.core.urlresolvers import reverse


def order_name(name):
    """order_name -- Limit a text to 20 chars length, if necessary strips the
    middle of the text and substitute it for an ellipsis.

    name -- text to be limited.

    """
    name = re.sub(r'^.*/', '', name)
    if len(name) <= 20:
        return name
    return name[:10] + "..." + name[-7:]


def serialize(instance, file_attr='file'):
    """serialize -- Serialize a Picture instance into a dict.

    instance -- Picture instance
    file_attr -- attribute name that contains the FileField or ImageField

    """
    obj = getattr(instance, file_attr)
    return {
        'url': obj.url,
        'name': order_name(obj.name),
        'type': mimetypes.guess_type(obj.path)[0] or 'image/png',
        'thumbnailUrl': obj.url,
        'size': obj.size,
        'deleteUrl': reverse('upload-delete', args=[instance.pk]),
        'deleteType': 'DELETE',
    }


def serialize_work_details(index, instance, file_attr='file'):
    print(instance)
    if hasattr(instance, file_attr):
        obj = getattr(instance, file_attr)
        img_url = obj.url
    else:
        img_url = instance

    return {
        'img': img_url,
        'alt': "{0} slide".format(index),
        'class': 'active' if index == 0 else '',
        'idx': "{0}".format(index),
    }


from .models import Images
import random

def serialize_search(apartment, file_attr='file'):
    print(apartment.name)
    # TODO use imageField in prop and remove this serialize
    image = Images.objects.filter(prop_id=apartment.id).first()
    if image is not None:
        img_url = getattr(image, file_attr).url
    else:
        img_url = random.choice(["/static/images/listing/list1.png","/static/images/listing/list2.png","/static/images/listing/list3.png"])
    return {
        'id' : apartment.id,
        'img' : img_url,
        'name' : apartment.name,
        'address' : apartment.address,
    }
