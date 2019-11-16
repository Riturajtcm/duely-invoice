from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Company
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE

class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'User Name'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))                                                      
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class CompanyForm(forms.ModelForm): 
    comapny_address = forms.CharField(widget=TinyMCE(attrs={'cols': 15, 'rows': 4})) 
    comapny_name = forms.CharField(widget=forms.TextInput(attrs={'class':' '}))
    company_website= forms.CharField(widget=forms.TextInput(attrs={'class':' '}))                                              
    class Meta:
        model = Company
        fields = ('comapny_name', 'comapny_address','company_website', 'logo','phone')        