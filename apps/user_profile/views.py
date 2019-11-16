from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .forms import SignUpForm ,CompanyForm
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.http import *
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:     
                old_users = User.objects.filter(email=form.data['email'])
                if old_users.count() > 0 :
                    form.add_error(None, "Email already exists !")
                    return render(request, 'signup.html', {'form': form})
                else :
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()
                    current_site = get_current_site(request)
                    subject = 'Activate Your Duly Account'
                    message = render_to_string('account_activation_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    res=user.email_user(subject, message,from_email="impiyush111@gmail.com")
                    return redirect('account_activation_sent',user=user)
            except Exception as e:
                print (e)
                form.add_error(None, "Error while creating account !")
                return render(request, 'signup.html', {'form': form})
        else:
            print(form.errors)    
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def account_activation_sent(request,user): 
    return render(request, 'account_activation_sent.html',{'username':user})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')



def user_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))

    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        try:
            if 'remember' in request.POST and request.POST['remember']:
                remember = request.POST['remember']
            else:
                remember = False
        except KeyError:
            remember = False
        try:     
            user=User.objects.get(username=username)
            if user is not None:
                if user.is_active : 
                    loginuser = authenticate(request , username=username, password=password)
                    if loginuser is not None:
                        login(request, loginuser)
                        if remember:
                            request.session.set_expiry(0)

                        return HttpResponseRedirect(reverse('home'))
                    else:
                        messages = []
                        messages.append(
                        {'tags': 'danger',
                        'text': 'Invalid username or password. Please try again.'
                        }
                        )
                        return render(request, 'login.html', {'messages': messages})        
                else:
                    messages = []
                    messages.append(
                        {'tags': 'danger',
                        'text': 'Please Confirm your Email .'
                        }
                        )
                    return render(request, 'login.html', {'messages': messages})
            else:
                messages = []
                messages.append(
                        {'tags': 'danger',
                        'text': 'Invalid username or password.Please try again.'
                        }
                    )
                return render(request, 'login.html', {'messages': messages})
        except Exception as e :
            messages = []
            messages.append(
                {'tags': 'danger',
                'text': 'Invalid username or password.Please try again.'
                }
                )
            return render(request, 'login.html', {'messages': messages})

    return render(request, 'login.html', {})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required(login_url=reverse_lazy('login'))
def profile_view(request):
    return render(request, 'user_profile/profile.html')

@login_required(login_url=reverse_lazy('login'))
def profile_Update_view(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST,request.FILES,instance=request.user.user_company)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            return render(request, 'user_profile/profile.html', {})
        else:
            print(form.errors)    
    else:
        form = CompanyForm(instance=request.user.user_company)
    return render(request, 'user_profile/profile_update.html', {'form': form})


