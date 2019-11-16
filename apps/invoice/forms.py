from django import forms
from .models import Invoice,InvoiceItem
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from customer.models import Customer


input_formats=['%Y-%m-%d',      # '2006-10-25'
'%m/%d/%Y',       # '10/25/2006'
'%m/%d/%y']

class InvoiceForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Invoice Title','class': 
                               'required  '}))
    invoive_no = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Invoice No#','class': 
                               'required form-control '}))
    invoice_date = forms.DateField(input_formats=input_formats)
    due_date = forms.DateField(input_formats=input_formats)
    tax = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Tax','class': 
                               'form-control datepicker ','required': 'false'}))
    discount = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Discount','class': 
                               'form-control datepicker ','required': 'false'}))
    notes = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Notes','class': 
                               'form-control datepicker ','required': 'false'}))
                                                                                                                
    class Meta:
        model = Invoice
        fields = ['title', 'invoive_no', 'customer', 'invoice_date', 'due_date', 'tax', 'discount', 'notes']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(InvoiceForm, self).__init__(*args, **kwargs)
        
        self.fields['tax'].required = False
        self.fields['discount'].required = False
        self.fields['notes'].required = False
        if user is not None:
            self.fields['customer'].queryset = Customer.objects.filter(user=user)

        

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = [ 'service', 'description', 'quantity', 'unit_price','price']

invoiceItemsformSet = inlineformset_factory(Invoice, InvoiceItem, fields=('service', 'description',
                      'quantity' ,'unit_price','price'), extra=1,
                       widgets={
          'service': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Service'}),
          'description': forms.TextInput(attrs={'class': 'required form-control ', 'placeholder': 'Description'}),
          'quantity': forms.TextInput(attrs={'class': 'required invoice_item_quantity form-control ', 'placeholder': 'Quantity'}),
          'unit_price': forms.TextInput(attrs={'class': 'required invoice_item_unit_price form-control ', 'placeholder': 'Unit Price'}),
          'price': forms.TextInput(attrs={'class': 'required invoice_item_price_total form-control', 'placeholder': 'Price'}),
                            }

         )        