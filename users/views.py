from django.shortcuts import render
from django.http import HttpResponseRedirect
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib import auth
from products.models import Basket
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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


class RegisterCreateView(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')





class ProfilUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id))

    def get_context_data(self, **kwargs):
        context = super(ProfilUpdateView, self).get_context_data()
        context['title'] = 'Rafistore-Profile'
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context

    def test_func(self):
        return self.request.user == self.get_object()




def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
