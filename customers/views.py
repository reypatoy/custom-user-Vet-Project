from django.shortcuts import render
from django.contrib import auth
from pathlib import Path

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import SignUpForm


def login_view(request):
    error_message = None
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))

                else:
                    if user.user_type == 1:
                        return redirect('crm:admin_dashboard_view')

                    if user.user_type == 2:
                        pass

                    if user.user_type == 3:
                        pass

        else:
            error_message = form.errors

    context = {
        'form': form,
        'error_message': error_message
    }

    return render(request, "auth/login.html", context)


def signup_view(request):
    errors = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('customers:signup_view')
        else:
            errors = form.errors
    else:
        form = SignUpForm()

    context = {
        'error_message': errors,
        'form': form
    }
    return render(request, "auth/signup.html", context)


def home_view(request):
    return render(request, "pages/home.html")


def appointment_view(request):
    return render(request, 'pages/appointment.html')
