from django.contrib.auth.mixins import PermissionRequiredMixin
from pets.models import pets
from .forms import add_staff_form
from accounts.models import (
    User as custom_user,
    customer as customer_user,
    staff as staff_user,
)
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.urls import reverse

# Create your views here.


class checkPremiumGroupMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="staff_group").exists():

            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/%s?next=%s" % ("staff/login/", request.path))


def staff_dashboard_view(request):
    if request.user.is_authenticated:
        if request.user.user_type != 2:
            logout(request)
            return redirect("/%s?next=%s" % ("staff/login/", request.path))

        else:
            return render(request, "staff/pages/staff_dashboard.html", {})
    else:
        return redirect("/%s?next=%s" % ("staff/login/", request.path))


def staff_login_view(request):
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

                if user.user_type == 2:
                    login(request, user)
                    if request.GET.get("next"):
                        return redirect(request.GET.get("next"))

                    else:
                        return redirect("staff:staff_dashboard_view")

                else:
                    invalid_login_error = "Invalid Account"

        else:
            error_message = form.errors
    context = {
        "title": "Login",
        "invalid_account": invalid_login_error,
        "form": form,
        "error_message": error_message,
    }
    return render(request, "staff/auth/login.html", context)


def staff_logout_view(request):
    logout(request)
    return redirect("staff:staff_login_view")


class add_pet_view(checkPremiumGroupMixin, SuccessMessageMixin, CreateView):
    model = pets
    success_message = "Pet Added Successfully!!!"
    fields = "__all__"
    template_name = "staff/pages/add_pets.html"


class add_pet_specific_customer_view(checkPremiumGroupMixin, CreateView):
    model = pets
    fields = ["pet_image", "pet_name", "breed", "age", "owner", "added_by"]
    template_name = "staff/pages/add_pet_specific_customer.html"

    def form_valid(self, form):
        customer = customer_user.objects.get(id=self.kwargs["pk"])
        pet = form.save(commit=False)
        pet.owner_id = customer
        pet.save()
        return redirect("staff:customers_list_view")


class pet_update_view(checkPremiumGroupMixin, SuccessMessageMixin, UpdateView):
    model = pets
    template_name = "staff/pages/pet_update.html"
    success_message = "Pet Updated Successfully!!!"
    fields = "__all__"


class pets_list_view(checkPremiumGroupMixin, ListView):
    model = pets
    template_name = "staff/pages/pets_list.html"
    paginate_by = 6

    def get_queryset(self):
        filter = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "id")
        if filter != "":
            if filter.isnumeric():
                cat = pets.objects.filter(Q(owner_id=filter)).order_by(order_by)
            else:
                cat = pets.objects.filter(
                    Q(pet_name__contains=filter)
                    | Q(breed__contains=filter)
                    | Q(owner__contains=filter)
                ).order_by(order_by)
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
    if request.user.is_authenticated:
        if request.user.user_type == 2:
            success_message = None
            staff_data = None
            error_message = None
            form = add_staff_form()
            if request.method == "POST":
                form = add_staff_form(request.POST, request.FILES)
                if form.is_valid():
                    username = form.cleaned_data.get("username")
                    first_name = form.cleaned_data.get("first_name")
                    last_name = form.cleaned_data.get("last_name")
                    contact_number = form.cleaned_data.get("contact_number")
                    address_barangay = form.cleaned_data.get("address_barangay")
                    address_municipality = form.cleaned_data.get("address_municipality")
                    profile_pic = form.cleaned_data.get("profile_pic")
                    email = form.cleaned_data.get("email")
                    User_instance = form.save()
                    current_staff = staff_user.objects.get(auth_user_id=User_instance)

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
                    User_instance.groups.add(1)
                    success_message = "Staff Added Successfully!!!"
                else:
                    error_message = form.errors
            context = {
                "success_message": success_message,
                "login_user": request.user.username,
                "staff": staff_data,
                "error_message": error_message,
                "form": form,
            }
            return render(request, "staff/pages/add_staff.html", context)
        else:
            return redirect("staff:staff_login_view")
    else:
        return redirect("/%s?next=%s" % ("staff/login/", request.path))


class staff_list_view(checkPremiumGroupMixin, ListView):
    model = staff_user
    template_name = "staff/pages/staff_list.html"
    paginate_by = 6

    def get_queryset(self):
        filter = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "auth_user_id_id")
        if filter is not None:
            cat = staff_user.objects.filter(
                Q(first_name__contains=filter) | Q(last_name__contains=filter)
            ).order_by(order_by)
        else:
            cat = staff_user.objects.all().order_by(order_by)
        return cat

    def get_context_data(self, **kwargs):
        context = super(staff_list_view, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "id")
        context["all_table_fields"] = staff_user._meta.get_fields()
        return context


class staff_update_view(checkPremiumGroupMixin, UpdateView):
    model = custom_user
    template_name = "staff/pages/staff_update.html"
    fields = ["first_name", "last_name", "username", "password", "password"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = staff_user.objects.get(auth_user_id=self.object.pk)
        context["staff"] = model
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()

        staff = staff_user.objects.get(auth_user_id=user.id)
        if self.request.FILES.get("profile_pic", False):
            profile_pic = self.request.FILES["profile_pic"]
            # fs = FileSystemStorage(location='/media/staff_profile_pictures/')
            # file_name = fs.save(profile_pic.name, profile_pic)
            # profile_pic_url = fs.url(file_name)
            staff.profile_pic = profile_pic
        staff.username = self.request.POST.get("username")
        staff.email = self.request.POST.get("email")
        staff.first_name = self.request.POST.get("first_name")
        staff.last_name = self.request.POST.get("last_name")
        staff.contact_number = self.request.POST.get("contact_number")
        staff.address_barangay = self.request.POST.get("address_barangay")
        staff.address_municipality = self.request.POST.get("address_municipality")
        staff.save()
        messages.success(self.request, "Staff Updated Successfully!!!")
        return HttpResponseRedirect(reverse("staff:staff_list_view"))


def staff_profile_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 2:
            id = request.GET.get("id")
            model = staff_user.objects.get(auth_user_id=id)
            context = {"staff": model}
            return render(request, "staff/pages/staff_profiles.html", context)
        else:
            return redirect("staff:staff_login_view")
    else:
        return redirect("/%s?next=%s" % ("staff/login/", request.path))


class customers_list_view(checkPremiumGroupMixin, ListView):
    model = customer_user
    template_name = "staff/pages/customers_list.html"
    paginate_by = 6

    def get_queryset(self):
        filter = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "id")
        if filter != "":
            cat = customer_user.objects.filter(
                Q(first_name__contains=filter)
                | Q(last_name__contains=filter)
                | Q(address_barangay__contains=filter)
                | Q(address_municipality__contains=filter)
            ).order_by(order_by)
        else:
            cat = customer_user.objects.all().order_by(order_by)
        return cat

    def get_context_data(self, **kwargs):
        context = super(customers_list_view, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "id")
        context["all_table_fields"] = customer_user._meta.get_fields()
        return context


def customers_profile_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 2:
            id = request.GET.get("id")
            context = None
            customer = customer_user.objects.get(id=id)
            pets_count = pets.objects.filter(owner_id=customer.id).count()
            context = {"customer": customer, "pets_count": pets_count}
            return render(request, "staff/pages/customers_profile.html", context)
        else:
            return redirect("/%s?next=%s" % ("staff/login/", request.path))
    else:
        return redirect("/%s?next=%s" % ("staff/login/", request.path))


class add_customer_view(SuccessMessageMixin, CreateView):
    model = custom_user
    fields = ["first_name", "last_name", "email", "username", "password"]
    template_name = "staff/pages/add_customer.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = 3
        user.set_password(form.cleaned_data["password"])
        user.save()

        profile_pic = self.request.FILES["profile_pic"]
        address_barangay = self.request.POST.get("address_barangay")
        address_municipality = self.request.POST.get("address_municipality")
        contact_number = self.request.POST.get("contact_number")
        user.customer.first_name = user.first_name
        user.customer.last_name = user.last_name
        user.customer.email = user.email
        user.customer.username = user.username
        user.customer.profile_pic = profile_pic
        user.customer.address_barangay = address_barangay
        user.customer.address_municipality = address_municipality
        user.customer.contact_number = contact_number
        user.customer.added_by = self.request.user.username
        user.save()
        messages.success(self.request, "Customer Added Successfully!!!")
        return redirect("staff:customers_list_view")
