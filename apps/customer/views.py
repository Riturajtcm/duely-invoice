from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from .models import Customer
from .forms import CustomerForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class CustomerListView(ListView):
    model = Customer
    context_object_name = 'customers_list'
    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user,deleted=False)

@method_decorator(login_required(login_url='/user/login/'), name='dispatch')
class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
     
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)    
      


class CustomerDetailView(DetailView):
    model = Customer


class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('customer_list')


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
