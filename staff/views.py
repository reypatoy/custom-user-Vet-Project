from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


from pets.forms import pets_form
from accounts.models import User, customer
# Create your views here.


def staff_dashboard_view(request):
    # if request.method == 'POST':
    form = pets_form()
    # if form.is_valid():
    context = {
        'title': 'staff dashboard',
        'form': form

    }
    return render(request, "staff/pages/staff_dashboard.html", context)


def staff_login_view(request):
    form = AuthenticationForm()
    return render(request, "staff/auth/login.html", {'form': form})


def staff_logout_view(request):
    logout(request)
    return redirect("staff:staff_login_view")


def add_pet_view(request):
    customers = customer.objects.all()
    return render(request, "staff/pages/add_pets.html", {'customers': customers})
