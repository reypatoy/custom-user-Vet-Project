from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q

from accounts.models import User, customer, staff
from .forms import add_staff_form
from pets.models import pets
# Create your views here.


def staff_dashboard_view(request):
    login_user = None
    if request.user.is_authenticated:
        if request.user.user_type == 2:
            login_user = request.user.username
            return render(request, "staff/pages/staff_dashboard.html", {'login_user': login_user})
        else:
            logout(request)
            return redirect('staff:staff_login_view')
    else:
        return redirect('staff:staff_login_view')


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
            error_message = form.errors
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


class add_pet_view(SuccessMessageMixin, CreateView):
    model = pets
    success_message = "Pet Added Successfully!!!"
    fields = "__all__"
    template_name = "staff/pages/add_pets.html"


class pets_list_view(ListView):
    model = pets
    template_name = "staff/pages/pets_list.html"
    paginate_by = 6

    def get_queryset(self):
        result = None
        filter = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "id")
        if filter != "":
            cat = pets.objects.filter(Q(pet_name__contains=filter) | Q(
                breed__contains=filter) | Q(owner__contains=filter)).order_by(order_by)
        else:
            cat = pets.objects.all().order_by(order_by)
        return cat

    def get_context_data(self, **kwargs):
        context = super(pets_list_view, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "id")
        context["all_table_fields"] = pets._meta.get_fields()
        return context


def add_staff_view(request):
    staff_data = None
    error_message = None
    form = add_staff_form()
    if request.method == 'POST':
        form = add_staff_form(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            contact_number = form.cleaned_data.get('contact_number')
            address_barangay = form.cleaned_data.get('address_barangay')
            address_municipality = form.cleaned_data.get(
                'address_municipality')
            profile_pic = form.cleaned_data.get('profile_pic')
            email = form.cleaned_data.get('email')
            User_instance = form.save()
            current_staff = staff.objects.get(auth_user_id=User_instance)

            current_staff.username = username
            current_staff.first_name = first_name
            current_staff.last_name = last_name
            current_staff.contact_number = contact_number
            current_staff.address_barangay = address_barangay
            current_staff.address_municipality = address_municipality
            current_staff.email = email
            current_staff.added_by = request.user.username
            current_staff.profile_pic = profile_pic

            current_staff.save()
        else:
            error_message = form.errors
    context = {
        'login_user': request.user.username,
        'staff': staff_data,
        'error_message': error_message,
        'form': form
    }
    return render(request, "staff/pages/add_staff.html", context)


class staff_list_view(ListView):
    model = staff
    template_name = "staff/pages/staff_list.html"
    paginate_by = 6

    def get_queryset(self):
        filter = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "auth_user_id_id")
        if filter is not None:
            cat = staff.objects.filter(Q(first_name__contains=filter) | Q(
                last_name__contains=filter)).order_by(order_by)
        else:
            cat = staff.objects.all().order_by(order_by)
        return cat

    def get_context_data(self, **kwargs):
        context = super(staff_list_view, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "id")
        context["all_table_fields"] = staff._meta.get_fields()
        return context
