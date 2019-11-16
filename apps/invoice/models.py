from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import FloatField
from django.db.models import TextField
from django_extensions.db.fields import AutoSlugField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models as models
from django_extensions.db import fields as extension_fields
from customer.models import Customer
from django.contrib.auth.models import User


class Invoice(models.Model):

    INVOICE_STATUS_CHOICES = (
    ("created", "CREATED"),
    ("SEND", "SEND"),
    ("DUE", "DUE"),
    ("PAID", "PAID"),
    ("OVERDUE", "OVERDUE"),
     )

    # Fields
    user = models.ForeignKey(
        User, null=True, blank=True,related_name='invoices',on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    slug = extension_fields.AutoSlugField(populate_from='invoive_no', blank=True)
    invoive_no = models.CharField(max_length=50)
    customer = models.ForeignKey(
        Customer, null=True, blank=True,related_name='invoices',on_delete=models.PROTECT)
    invoice_date = models.DateTimeField()
    due_date = models.DateTimeField()
    tax = models.FloatField()
    discount = models.FloatField()
    notes = models.TextField(max_length=500)
    status = models.CharField(max_length=20)


    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('invoice_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('invoice_update', args=(self.slug,))

class InvoiceItem(models.Model):

    # Fields
    slug = extension_fields.AutoSlugField(populate_from='service', blank=True)
    invoice = models.ForeignKey(
        Invoice, null=True, blank=True,related_name='invoice_items',on_delete=models.PROTECT)
    service = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    quantity = models.FloatField()
    unit_price = models.FloatField()
    price = models.FloatField()


    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('invoice_item_invoiceitem_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('invoice_item_invoiceitem_update', args=(self.slug,))

