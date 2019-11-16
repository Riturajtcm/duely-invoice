from django.urls import path, include




from . import views




urlpatterns = (
    # urls for Invoice
    path('invoices/', views.InvoiceListView.as_view(), name='invoice_list'),
    path('create/', views.InvoiceCreateView.as_view(), name='invoice_create'),
    path('detail/<slug:slug>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('update/<slug:slug>/', views.InvoiceUpdateView.as_view(), name='invoice_update'),
)
