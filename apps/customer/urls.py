from django.urls import path, include

from . import views



urlpatterns = (
    # urls for Customer
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('detail/<slug:slug>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('update/<slug:slug>/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('delete/<slug:slug>/', views.CustomerDeleteView.as_view(), name='customer_delete'),
)
