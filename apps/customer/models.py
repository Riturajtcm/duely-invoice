from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.db.models import CharField
from django.db.models import TextField
from django_extensions.db.fields import AutoSlugField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models as models
from django_extensions.db import fields as extension_fields
from framework.models import BaseModel
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Customer(BaseModel):

    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    user = models.ForeignKey(
        User, null=True, blank=True,related_name='cutomers',on_delete=models.PROTECT)
    address = models.TextField(max_length=200)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    point_of_contact = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    country = CountryField()
    webiste = models.CharField(max_length=50)


    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.slug

    def __str__(self):
        return '{}-{}'.format(self.name, self.email)    

    def get_absolute_url(self):
        return reverse('customer_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('customer_update', args=(self.slug,))

