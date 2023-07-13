from django.shortcuts import render
from django.http import HttpResponseRedirect
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.urls import reverse
from django.contrib import auth
from products.models import Basket


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()

    context = {'form': form}

    return render(request, 'users/login.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()

    context = {'form': form}

    return render(request, 'users/register.html', context)


def profile(request):
    if request.method == "POST":
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'form': form,
        'title': 'Profile',
        'baskets': Basket.objects.filter(user=request.user)
              }

    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
