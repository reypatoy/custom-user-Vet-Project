from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


from pets.forms import pets_form
from accounts.models import User, customer, staff
from .forms import add_staff_form
# Create your views here.


def staff_dashboard_view(request):
    # if request.user.is_authenticated:
    #     if request.user.user_type == 2:
    return render(request, "staff/pages/staff_dashboard.html", {})
    #     else:
    #         return redirect('staff:staff_login_view')
    # else:
    #     return redirect('staff:staff_login_view')


def staff_login_view(request):
    invalid_login_error = None
    error_message = None
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))

                else:
                    if user.user_type == 2:
                        login(request, user)
                        return redirect('staff:staff_dashboard_view')
                    else:
                        invalid_login_error = "Invalid Account"

        else:
            error_message = 'hello'
    context = {
        'title': 'Login',
        'invalid_account': invalid_login_error,
        'form': form,
        'error_message': error_message
    }
    return render(request, "staff/auth/login.html", context)


def staff_logout_view(request):
    logout(request)
    return redirect("staff:staff_login_view")


def add_pet_view(request):
    customers = customer.objects.all()
    return render(request, "staff/pages/add_pets.html", {'customers': customers})


def add_staff_view(request):
    staff_data = None
    error_message = None
    form = add_staff_form()
    if request.method == 'POST':
        form = add_staff_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            contact_number = form.cleaned_data.get('contact_number')
            address_barangay = form.cleaned_data.get('address_barangay')
            address_municipality = form.cleaned_data.get(
                'address_municipality')
            email = form.cleaned_data.get('email')
            form.save()
            staff_data = User.objects.get(
                username=username)

            obj = staff.objects.create(
                first_name=first_name,
                last_name=last_name,
                contact_number=contact_number,
                address_barangay=address_barangay,
                address_municipality=address_municipality,
                email=email,
                auth_user_id_id=40
            )

            obj.save()
        else:
            error_message = form.errors
    context = {
        'staff': staff_data,
        'error_message': error_message,
        'form': form
    }
    return render(request, "staff/pages/add_staff.html", context)
