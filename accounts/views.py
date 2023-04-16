from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout,login
from django.contrib import messages
from .forms import LoginForm
from .auth import unauthenticated_user
from .models import Profile
from .forms import ProfileForm

# Create your views here.

@unauthenticated_user
def register_user(request):
    if request.user.is_authenticated:
        return redirect('/products/test')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, username= user.username)
            messages.add_message(request, messages.SUCCESS, "User registered successfully")
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Eroor in registering user')
            return render (request, 'accounts/register.html',{'form':form})
    context = {
            'form': UserCreationForm
        }
    return render(request, 'accounts/register.html', context)

def logout_user(request):
    logout(request)
    return redirect('/')

@unauthenticated_user
def login_user(request):
    if request.user.is_authenticated:
        return redirect('')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,username=data['username'], password=data['password'])

            print(user)
            if user is not None:
                if not user .is_staff:
                 login(request,user)
                 return redirect('')
                elif user .is_staff:
                    login(request, user)
                    return redirect('/admin-dashboard')


            else:
                messages.add_message(request, messages.ERROR, 'Usename or password is invalid')
                return render(request,'accounts/login.html',{'form':form})
    context = {
        'form': LoginForm
    }

    return render(request,'accounts/login.html', context)

def user_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Update Successful for ' + str(request.user.profile))
            return redirect('/profile')
    context = {'form': form}
    return render(request, 'accounts/profile.html', context)