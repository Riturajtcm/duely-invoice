from django.urls import path, include,re_path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = (
    # urls for Customer
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile_update/', views.profile_Update_view, name='profile_update'),
    path('account_activation_sent/(?P<user>[^\/]*)', views.account_activation_sent, name='account_activation_sent'),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.activate, name='activate'),
)
