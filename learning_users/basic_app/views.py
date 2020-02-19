from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'basic_app/index.html')


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = _save_user(user_form)
            _save_user_profile(profile_form, request, user)
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    form_dict = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
    }
    return render(request, 'basic_app/registration.html', form_dict)


def user_login(request):
    if request.method != 'POST':
        return render(request, 'basic_app/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)
    if not user:
        print("Someone tried to login and failed")
        return HttpResponse("Invalid login detauls supplied")

    if user.is_active:
        login(request, user)
        return HttpResponseRedirect(reverse('index'))

    return HttpResponse("ACCOUNT NOT ACTIVE")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def _save_user_profile(profile_form, request, user):
    profile = profile_form.save(commit=False)
    profile.user = user
    if 'profile_pic' in request.FILES:
        profile.profile_pic = request.FILES['profile_pic']
    profile.save()


def _save_user(user_form):
    user = user_form.save()
    user.set_password(user.password)
    user.save()
    return user
