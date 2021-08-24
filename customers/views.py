from django.shortcuts import render
from django.contrib import auth
from pathlib import Path

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .forms import SignUpForm
from accounts.models import User, customer as customer_user
from blogs.models import Blogs as doctors_blogs
from appointments.models import Appointment as customers_appointment
from django.http import HttpResponse


def login_view(request):
    users = None
    invalid_login_error = None
    error_message = None
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                users = customer_user.objects.all()
                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))

                else:
                    if user.user_type == 3:
                        login(request, user)
                        return redirect("customers:dashboard_view")
                    else:
                        invalid_login_error = "Invalid Account"

        else:
            error_message = "Error Login"
    context = {
        "users": users,
        "title": "Login",
        "invalid_account": invalid_login_error,
        "form": form,
        "error_message": error_message,
    }
    return render(request, "auth/login.html", context)


def signup_view(request):

    errors = None
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            raw_password = form.cleaned_data.get("password1")

            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            contact_number = form.cleaned_data.get("contact_number")
            address_barangay = form.cleaned_data.get("address_barangay")
            address_municipality = form.cleaned_data.get("address_municipality")
            profile_pic = form.cleaned_data.get("profile_pic")
            email = form.cleaned_data.get("email")
            User_instance = form.save()
            current_customer = customer_user.objects.get(auth_user_id=User_instance)

            current_customer.first_name = first_name
            current_customer.last_name = last_name
            current_customer.contact_number = contact_number
            current_customer.address_barangay = address_barangay
            current_customer.address_municipality = address_municipality
            current_customer.email = email
            current_customer.profile_pic = profile_pic

            current_customer.save()

            user = authenticate(username=email, password=raw_password)
            login(request, user)
            return redirect("customers:dashboard_view")
        else:
            errors = form.errors
    else:
        form = SignUpForm()

    context = {"title": "Signup", "error_message": errors, "form": form}
    return render(request, "auth/signup.html", context)


def dashboard_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 3:
            return render(request, "pages/customers_dashboard.html")
        else:
            return redirect("customers:login_view")
    else:
        return redirect("customers:login_view")


def logout_view(request):
    logout(request)
    return redirect("customers:home_view")


def home_view(request):
    return render(request, "pages/home.html", {"title": "Home"})


def appointment_view(request):
    if request.user.is_authenticated and request.user.user_type == 3:
        return render(request, "pages/appointment.html", {})
    else:
        return redirect("customers:login_view")


def blogs_view(request):
    blogs = doctors_blogs.objects.all()
    return render(request, "pages/blogs.html", {"blogs": blogs})


def verefy_schedule_view(request):
    if request.method == "POST":
        schedule = request.POST.get("schedule")
        verefy = customers_appointment.objects.filter(schedule=schedule).count()
        return HttpResponse(verefy)


def save_appointment_view(request):
    appointments = customers_appointment.objects.all()
    max = 0
    for appointment in appointments:
        if appointment.id > max:
            max = appointment.id
    if request.method == "POST":
        description = request.POST.get("description")
        schedule = request.POST.get("schedule")
        new_appointment = customers_appointment.objects.create(
            id=max + 1,
            description=description,
            schedule=schedule,
            customer=request.user.customer,
        )
        new_appointment.save()
    return HttpResponse(
        "Please Check Your Email For Further Info About Your Appointment"
    )
