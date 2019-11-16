from django.core.mail import send_mail
from django.template.loader import get_template
import os  
from email.mime.image import MIMEImage

from django.core.mail import EmailMultiAlternatives  
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders

def sendInvoiceMail(invoice_obj, company_obj, invoice_items_obj, customer_obj ):
    context_data ={}
    invoices=[]
    context_data['company_name']=company_obj.comapny_name
    context_data['company_address']=company_obj.comapny_address
    context_data['customer_name']=customer_obj.name
    context_data['customer_address']=customer_obj.address
    context_data['customer_email']=customer_obj.email
    context_data['invoice_date']=invoice_obj.invoice_date
    context_data['due_date']=invoice_obj.due_date
    for invoice_item in invoice_items_obj:
        invoice_data={}
        invoice_data['service']=invoice_item.service
        invoice_data['description']=invoice_item.description
        invoice_data['quantity']=invoice_item.quantity
        invoice_data['unit_price']=invoice_item.unit_price
        invoice_data['price']=invoice_item.price
        invoices.append(invoice_data)

    context_data['invoice_items']=invoices
    context_data['imgage_file'] = company_obj.logo
    htmly = get_template('invoice.html')
    html_content = htmly.render(context_data)
    # send_mail(
    #             'Iovoice',
    #             "plain_message",
    #             'impiyush111@gmail.com',
    #         ['piyushrajmani@gmail.com'],
    #         fail_silently=False,
    #         html_message=html_content
    #     )

    msg = EmailMultiAlternatives("Iovoice", html_content, "impiyush111@gmail.com", ["piyushrajmani@gmail.com"])
    msg.content_subtype = 'html'  # Main content is text/html  
    msg.mixed_subtype = 'related'  # This is critical, otherwise images will be displayed as attachments!
    imgage_file = company_obj.logo
    with open(imgage_file.path, 'rb') as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data)
    logo.add_header('Content-ID', '<{}>'.format(imgage_file))
    msg.attach(logo)
    msg.send()    