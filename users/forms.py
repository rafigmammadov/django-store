from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control py-4', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter '
                                                                                                            'your '
                                                                                                            'first '
                                                                                                            'name'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter your last name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter a '
                                                                                                          'username'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter your e-mail'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter '
                                                                                                               'a '
                                                                                                               'password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control py-4', 'placeholder': 'Enter the password again'}))


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)

    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False, )

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': True}))


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')

