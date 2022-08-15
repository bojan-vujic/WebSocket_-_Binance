from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from main.models import Profile
from django.conf import settings


attrs = {'class': 'form-control'}

class UserForm(forms.Form, forms.ModelForm):
  # The class 'form-control' is a bootstrap class
  username = forms.CharField(
    required = True, min_length = 4, max_length = 16,
    widget   = forms.TextInput(attrs=attrs),
  )
  email    = forms.EmailField(widget=forms.EmailInput(attrs=attrs))
  password = forms.CharField(
    required = True, min_length = settings.MIN_PASSWORD_LENGHT,
    widget=forms.PasswordInput(attrs=attrs)
  )
  
  class Meta():
    model  = User
    fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
  image = forms.ImageField(
    required=False,
    widget=forms.FileInput(attrs={'class': 'form-control custom-file-input'})
  )

  class Meta():
    model  = Profile
    fields = ['image']

