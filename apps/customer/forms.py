from django import forms
from .models import Customer
from django_countries.fields import CountryField


class CustomerForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '','class': 
                               'required'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '','class': 
                               'required '}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '','class': 
                               'required'}))
    point_of_contact = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '','class':''}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '','class':''}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '','class':''}))
    state = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '','class':''}))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '','class':''}))
    country = CountryField().formfield()
    website = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '','class':''}))                                                                                                        
    class Meta:
        model = Customer
        fields = ['name', 'address', 'email', 'point_of_contact','phone','city','state','zip_code','country','website']

class anonymousCompanyForm(forms.Form):
    company_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Company Name','class': 
                               'required'}))
    company_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address','class': 
                               'required'}))
    company_telephone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Telephone','class': 
                               'required'}))
    company_email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email','class': 
                               'required'}))