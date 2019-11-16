from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Invoice
from .forms import InvoiceForm, invoiceItemsformSet
from customer.forms import CustomerForm,anonymousCompanyForm
from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils.html import strip_tags
from django import forms
from customer.models import Customer
from django.http import HttpResponse
from .util import sendInvoiceMail
from user_profile.models import Company
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class InvoiceListView(ListView):
    model = Invoice
    paginate_by = 10
    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)

class InvoiceCreateView(CreateView):
    model = Invoice
    form_class = InvoiceForm

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['invoice_form'] = InvoiceForm(self.request.POST)
            context['invoice_item_form_set'] = invoiceItemsformSet(self.request.POST)
        else:
            context['invoice_form'] = InvoiceForm(user=self.request.user)  
            context['invoice_item_form_set'] = invoiceItemsformSet(instance=Invoice())
        return context
    

    def form_valid(self, form):
        context = self.get_context_data()
        invoice_form = context['invoice_form']
        invoice_item_form_set = context['invoice_item_form_set']
        if invoice_form.is_valid() and invoice_item_form_set.is_valid():
            self.object = invoice_form.save(commit=False)
            invoice_item_form_set.instance = self.object
            self.object.user=self.request.user
            self.object.save()
            invoce_item_objs=invoice_item_form_set.save()
            user_company=Company.objects.get(user=self.request.user)
            sendInvoiceMail(self.object,user_company,invoce_item_objs,self.object.customer)
            return HttpResponse('Mail successfully sent')
        else:
            print(invoice_item_form_set.errors)
            return self.render_to_response(self.get_context_data(invoice_form=invoice_form,invoice_item_form_set=invoice_item_form_set))
    

# class InvoiceCreateView(CreateView):
#     model = Invoice
#     form_class = InvoiceForm

#     def get_template_names(self):
#         if not self.request.user.is_anonymous:
#            return ['invoice/invoice_form.html']
#         else:
#            return ['invoice/anonymous_user_invoice.html']

#     # def get_form(self):
#     #     """
#     #     Returns an instance of the form to be used in this view.
#     #     """
#     #     form = self.form_class(**self.get_form_kwargs())
#     #     if not self.request.user.is_anonymous:
#     #         form.fields['customer'] = forms.ModelChoiceField(
#     #             queryset=Customer.objects.filter(user=self.request.user),widget=forms.Select(attrs={'class':''}))
#     #     return form      

#     def get_context_data(self, **kwargs):
#         context = super(InvoiceCreateView, self).get_context_data(**kwargs)
#         if self.request.POST:
#             context['invoice_form'] = InvoiceForm(self.request.POST)
#             context['invoice_item_form_set'] = invoiceItemsformSet(self.request.POST)
#             if self.request.user.is_anonymous:
#                 context['cutomer_form']=CustomerForm(self.request.POST)
#                 context['anonymous_company_form']= anonymousCompanyForm(self.request.POST)
#         else:
#             context['invoice_form'] = InvoiceForm(user=self.request.user)  
#             context['invoice_item_form_set'] = invoiceItemsformSet(instance=Invoice())
#             if self.request.user.is_anonymous:
#                 context['cutomer_form']=CustomerForm()
#                 context['anonymous_company_form']= anonymousCompanyForm()
        
#         return context

#     def form_valid(self, form):
#         if self.request.user.is_anonymous:
#             context = self.get_context_data()
#             invoice_form = context['invoice_form']
#             customer_form=context['cutomer_form']
#             anonymous_company_form=context['anonymous_company_form']
#             invoice_item_form_set = context['invoice_item_form_set']
#             if invoice_form.is_valid() and invoice_item_form_set.is_valid() and anonymous_company_form.is_valid():
#                 self.object = invoice_form.save(commit=False)
#                 invoice_item_form_set.instance = self.object
#                 invoice_form_data=invoice_item_form_set.save(commit=False)
#                 cutomer_obj=customer_form.save(commit=False)
#                 company_obj = anonymous_company_form.cleaned_data
#                 context_data ={}
#                 invoices=[]
#                 context_data['company_name']=company_obj['company_name']
#                 context_data['company_address']=company_obj['company_address']
#                 context_data['company_telephone']=company_obj['company_telephone']
#                 context_data['company_email']=company_obj['company_email']
#                 context_data['customer_name']=cutomer_obj.name
#                 context_data['customer_address']=cutomer_obj.address
#                 context_data['customer_email']=cutomer_obj.email
#                 context_data['invoice_date']=self.object.invoice_date
#                 context_data['due_date']=self.object.due_date
#                 for invoice_item in invoice_form_data:
#                     invoice_data={}
#                     invoice_data['service']=invoice_item.service
#                     invoice_data['description']=invoice_item.description
#                     invoice_data['quantity']=invoice_item.quantity
#                     invoice_data['unit_price']=invoice_item.unit_price
#                     invoice_data['price']=invoice_item.price
#                     invoices.append(invoice_data)

#                 context_data['invoice_items']=invoices
#                 htmly = get_template('invoice.html')
#                 html_content = htmly.render(context_data)
#                 send_mail(
#                          'Subject',
#                          "plain_message",
#                          'impiyush111@gmail.com',
#                         ['piyushrajmani@gmail.com'],
#                         fail_silently=False,
#                         html_message=html_content
#                 )

#                 return HttpResponse('Mail successfully sent')
                
#             else:
#                 print ("invalid form")
#                 print(invoice_item_form_set.errors)
#                 return self.render_to_response(self.get_context_data(invoice_form=invoice_form,invoice_item_form_set=invoice_item_form_set,
#                              customer_form=customer_form,anonymous_company_form=anonymous_company_form))
        
#         else:
#             context = self.get_context_data()
#             invoice_form = context['invoice_form']
#             invoice_item_form_set = context['invoice_item_form_set']
#             if invoice_form.is_valid() and invoice_item_form_set.is_valid():
#                 self.object = invoice_form.save(commit=False)
#                 invoice_item_form_set.instance = self.object
#                 self.object.user=self.request.user
#                 self.object.save()
#                 invoce_item_objs=invoice_item_form_set.save()
#                 user_company=Company.objects.get(user=self.request.user)
#                 sendInvoiceMail(self.object,user_company,invoce_item_objs,self.object.customer)
#                 return HttpResponse('Mail successfully sent')
#             else:
#                 print(invoice_item_form_set.errors)
#                 return self.render_to_response(self.get_context_data(invoice_form=invoice_form,invoice_item_form_set=invoice_item_form_set))    

#     def form_invalid(self, form):
#         if self.request.user.is_anonymous:
#             print ("inside anonymous invalid ")
#             print (form.errors)
#             context = self.get_context_data()
#             invoice_form = context['invoice_form']
#             invoice_item_form_set = context['invoice_item_form_set']
#             customer_form=context['cutomer_form']
#             anonymous_company_form=context['anonymous_company_form']
#             return self.render_to_response(self.get_context_data(invoice_form=invoice_form,invoice_item_form_set=invoice_item_form_set,
#                          customer_form=customer_form,anonymous_company_form=anonymous_company_form))
#         else:
#             print ("inside logedin invalid ")
#             print (form.errors)
#             context = self.get_context_data()
#             invoice_form = context['invoice_form']
#             invoice_item_form_set = context['invoice_item_form_set']
#             return self.render_to_response(self.get_context_data(invoice_form=invoice_form,invoice_item_form_set=invoice_item_form_set))



class InvoiceDetailView(DetailView):
    model = Invoice


class InvoiceUpdateView(UpdateView):
    model = Invoice
    form_class = InvoiceForm
