
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponse


class BaseListView(ListView):
    paginate_by = 10
    default_sort_field = 'id'
    allowed_sort_fields = {default_sort_field: {'default_direction': '+',
                                                'verbose_name': 'ID'}}

    def get_queryset(self):
        if self.request.GET:
            queryset = self.filter_class(self.request.GET,
                                         queryset=self.model.objects.all()).qs
        else:
            queryset = self.model.objects.all()
        return queryset


class LoginRequiredView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
