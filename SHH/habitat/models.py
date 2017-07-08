from django.db import models
from django.utils import timezone

# https://github.com/alex/django-taggit
from taggit.managers import TaggableManager
# https://pypi.python.org/pypi/django-multiselectfield/
from multiselectfield import MultiSelectField
from django.utils.translation import gettext as _

from django.contrib.auth import get_user_model
User = get_user_model()

class Contact(models.Model):
    '''
        Contacts
    '''
    line1 = models.CharField(max_length=150)
    line2 = models.CharField(max_length=150)
    postalcode = models.CharField(max_length=10)
    city = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=18)

    def __str__(self):
        pass


class Property(models.Model):
    '''
        Basic information of the properties
        我们可能需要一个 物业类型/地址/面积/房型（studio/1br/2br/3br）/租金价格/联系方式（eMail）/然后和一个features(big balcony/new renovation/)
    '''
    FEATURE_CHOICES = (('item_key1', _('Item title 1.1')),
                       ('item_key2', _('Item title 1.2')),
                       ('item_key3', _('Item title 1.3')),
                       ('item_key4', _('Item title 1.4')),
                       ('item_key5', _('Item title 1.5')),
                       )

    OLD_HOUSE = 'old_house'
    HIGH_RISE = 'high_rise'
    VILLA = 'villa'
    SERVICE_APT = 'service_apt'

    PROPERTY_CHOICES = (
        (OLD_HOUSE, _('Old house')),
        (HIGH_RISE, _('High-rise')),
        (VILLA, _('Villa')),
        (SERVICE_APT, _('Service Apartment')),
    )

    STUDIO = 'studio'
    LOFT = 'loft'
    ONE_BR = 'one_br'
    TWO_BR = 'two_br'
    THREE_BR = 'three_br'
    FOUR_BR_PLUS = 'four_br_plus'

    ROOM_CHOICE = ((STUDIO, _('Studio')),
                   (LOFT, _('Loft')),
                   (ONE_BR, _('1BR')),
                   (TWO_BR, _('2BR')),
                   (THREE_BR, _('3BR')),
                   (FOUR_BR_PLUS, _('4BR+')),
                   )

    name = models.CharField('Your property name:',
                            default='', max_length=50, blank=True)
    #description = models.TextField()
    address = models.CharField(
        '* Input your address', max_length=50, blank=False)
    room_type = models.CharField(
        '* Select Room Type', blank=False, max_length=50, default='0', choices=ROOM_CHOICE)
    property_type = models.CharField(
        '* Select Property Type', blank=False, max_length=50, default='0', choices=PROPERTY_CHOICES)
    size = models.FloatField('* Room Size', blank=False)
    price = models.IntegerField('* Price', blank=False)
    pub_date = models.DateTimeField(default=timezone.now)
    #contact = models.ForeignKey(Contact)
    email = models.EmailField('* Email', blank=False)
    phone = models.CharField('* Phone', blank=False, max_length=18)
    features = MultiSelectField(_("Features"), choices=FEATURE_CHOICES,
                                max_choices=3,
                                max_length=300, null=True)
    submitted = models.BooleanField(default=False)
    # TODO add user
    #user = models.ForeignKey(User)
    
    def __str__(self):
        return "property_id:{0}".format(self.id)


'''
# Obsolete
class Feature(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    #https://docs.djangoproject.com/en/1.11/topics/db/examples/many_to_many/
    properties = models.ManyToManyField(Property)

    def __str__(self):
        pass
'''


def get_image_file(instance, filename):
    return '/'.join(['content', instance.user.id, str(instance.prop_id), filename])


def get_image_file_by_id(instance, filename):
    return '/'.join(['content', str(instance.prop_id), filename])


class Images(models.Model):
    '''
        Images of the properties
        Reference: https://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django
    '''
    '''
    prop = models.ForeignKey(Property, default=None)
    image = models.ImageField(upload_to=get_image_file, verbose_name='Image')

    def __str__(self):
        pass

    '''
    #
    
    # TODO add user after can read data
    #user = models.ForeignKey(User)
    # TODO add this after user can add
    #file = models.ImageField(upload_to=get_image_file, verbose_name='Image', blank=True, null=True)
    
    prop_id = models.IntegerField(default=-1)
    #file = models.ImageField(upload_to="pictures", verbose_name='Image', blank=True, null=True)
    file = models.ImageField(upload_to=get_image_file_by_id, verbose_name='Image', blank=True, null=True)
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(Images, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.file.delete(False)
        super(Images, self).delete(*args, **kwargs)


class Comment(models.Model):
    prop = models.ForeignKey(Property, default=None)
    comment = models.TextField()

    def __str__(self):
        pass
