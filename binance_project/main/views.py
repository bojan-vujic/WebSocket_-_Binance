from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from main.forms import UserForm, UserProfileForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError



User._meta.get_field('email')._unique = True

def index(request):
    context = {}
    return render(request, 'main/index.html', context)


def signup(request):
    registered = False
    user_form = UserForm()

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            ###########
            user = user_form.save(commit=False)
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']

            try:
                validate_password(password, user)
            except ValidationError as e:
                # to be displayed with the field's errors
                user_form.add_error('password', e)
                context = {
                    'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered,
                    'first_two' : ['username', 'email'],
                }
                return render(request, 'main/signup.html', context)
            ##################
            
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
                profile.save()
            registered = True
            
            # automatic login after creating an account
            auth_login(request, user)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
        'first_two': ['username', 'email'],
    }

    return render(request, 'main/signup.html', context)


def user_login(request):
    context = {
        'username' : 'ok',
        'password' : 'ok'
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            context['username'] = False

        # use django authentication function
        user = authenticate(username=username, password=password)
        
        try:
            validate_password(password, user)
        except ValidationError as e:
            context['password'] = 'not'

        # check if user passed the authentication process
        if user:
            context['username'] = 'ok'
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Account not active")
        else:
            messages.error(request, 'Invalid login details!')
            return render(request, 'main/login.html', context)
    return render(request, 'main/login.html', context)


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'main/logout.html', {})


