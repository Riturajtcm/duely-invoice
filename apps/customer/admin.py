from django.contrib import admin
from django import forms
from .models import Customer

class CustomerAdminForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'


class CustomerAdmin(admin.ModelAdmin):
    form = CustomerAdminForm
    list_display = ['name', 'slug', 'user', 'address',  'email', 'point_of_contact']
    readonly_fields = ['name', 'slug', 'user', 'address', 'email', 'point_of_contact']

admin.site.register(Customer, CustomerAdmin)
