from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            return
        data = form.cleaned_data
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse("Muvaffaqiyatli kirish amalga oshirildi!")
            else:
                return HttpResponse("User active emas!")
        else:
            return HttpResponse("Login yoki parol xato kiritildi!")
    else:
        form = LoginForm()
        context = {
            'form': form,
        }

        return render(request, 'registration/login.html', context)

@login_required
def dashboard_view(request):
    user = request.user
    context = {
        'user': user,
        'profile': user.profile,
    }

    return render(request, 'pages/user_profile.html', context)


def user_registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                'user': new_user,
            }

            return render(request, 'account/register_done.html', context)
        else:
            return HttpResponse("Iltimos, ma'lumotlarni to'g'ri to'ldiring!")
    else:
        form = UserRegistrationForm()
        context = {
            'form': form,
        }

        return render(request, 'account/register.html', context)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/register.html'


def edit_user(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, "account/profile_edit.html", context)
