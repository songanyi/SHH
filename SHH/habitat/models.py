from django.db import models

#https://github.com/alex/django-taggit
from taggit.managers import TaggableManager

'''
    Contacts
'''
class Contact(models.Model):
    line1 = models.CharField(max_length=150)
    line2 = models.CharField(max_length=150)
    postalcode = models.CharField(max_length=10)
    city = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=18)

    def __str__(self):
        pass

'''
    Basic information of the properties
'''
class Property(models.Model):
    address = models.TextField()
    size = models.FloatField()
    pub_date = models.DateTimeField('date published')
    contact = models.ForeignKey(Contact)
    tags = TaggableManager()

    def __str__(self):
        pass


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

'''
    Images of the properties
    Reference: https://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django
'''

def get_image_file(instance, filename):
    return '/'.join(['content', instance.user.username, filename])


class Images(models.Model):
    prop = models.ForeignKey(Property, default=None)
    image = models.ImageField(upload_to=get_image_file, verbose_name='Image')

    def __str__(self):
        pass
