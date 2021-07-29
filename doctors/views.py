from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages

from accounts.models import (
    customer as customer_user,
    User as custom_user,
    staff as staff_user,
)
from pets.models import pets


# Create your views here.


class CheckGroupPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 1:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("/%s?next=%s" % ("doctors/login/", request.path))
        else:
            return redirect("/%s?next=%s" % ("doctors/login/", request.path))


def doctors_login_view(request):
    status = None
    context = None
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.user_type == 1:
                    login(request, user)
                    if request.GET.get("next"):
                        return redirect(request.GET.get("next"))
                    else:
                        return redirect("doctors:doctors_dashboard_view")
                else:
                    status = "Invalid Account!!!"
        else:
            status = form.errors
            form = AuthenticationForm()
    context = {"status": status, "form": form}
    return render(request, "doctors/auth/login.html", context)


def doctors_dashboard_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return render(request, "doctors/pages/doctors_dashboard.html", {})
        else:
            return redirect("doctors:doctors_login_view")
    else:
        return redirect("/%s?next=%s" % ("doctors/login/", request.path))
        # return HttpResponseRedirect("doctors:doctors_login_view")


def doctors_logout_view(request):
    logout(request)
    return redirect("doctors:doctors_login_view")


class pets_list_view(CheckGroupPermissionMixin, ListView):
    model = pets
    template_name = "doctors/pages/pets_list.html"
    paginate_by = 6

    def get_queryset(self):
        filter = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "id")
        if filter != "":
            if filter.isnumeric():
                cat = pets.objects.filter(owner_id=filter).order_by(order_by)
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


class add_pet_view(CheckGroupPermissionMixin, CreateView):
    model = pets
    template_name = "doctors/pages/add_pet.html"
    fields = ["pet_image", "pet_name", "breed", "age", "owner", "added_by", "owner_id"]

    def form_valid(self, form):
        pets_id = pets.objects.all()
        max = 0
        for id in pets_id:
            if id.id > max:
                max = id.id
        pet = form.save(commit=False)
        pet.id = max + 1
        pet.save()
        return redirect("doctors:pets_list_view")


class add_pet_specific_customer_view(CheckGroupPermissionMixin, CreateView):
    model = pets
    template_name = "doctors/pages/add_pet_specific_customer.html"
    fields = ["pet_image", "pet_name", "breed", "age", "owner", "added_by"]

    def form_valid(self, form):
        pets_id = pets.objects.all()
        max = 0
        for id in pets_id:
            if id.id > max:
                max = id.id
        customer = customer_user.objects.get(id=self.kwargs["pk"])
        pet = form.save(commit=False)
        pet.owner_id = customer
        pet.id = max + 1
        pet.save()
        return redirect("doctors:customers_list_view")


class update_pet(CheckGroupPermissionMixin, UpdateView):
    model = pets
    template_name = "doctors/pages/pet_update.html"
    success_message = "Pet Updated Successfully!!!"
    fields = ["pet_image", "pet_name", "breed", "age", "owner", "added_by"]

    def form_valid(self, form):
        form.save()
        return redirect("doctors:pets_list_view")


class customers_list(CheckGroupPermissionMixin, ListView):
    model = customer_user
    template_name = "doctors/pages/customers_list.html"
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
        context = super(customers_list, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "id")
        context["all_table_fields"] = customer_user._meta.get_fields()
        return context


class add_customer_view(CheckGroupPermissionMixin, SuccessMessageMixin, CreateView):
    model = custom_user
    template_name = "doctors/pages/add_customer.html"
    fields = ["first_name", "last_name", "email", "username", "password"]

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = 3
        user.set_password(form.cleaned_data["password"])
        user.save()

        user.customer.first_name = user.first_name
        user.customer.last_name = user.last_name
        user.customer.email = user.email
        user.customer.username = user.username
        user.customer.profile_pic = self.request.FILES["profile_pic"]
        user.customer.contact_number = self.request.POST.get("contact_number")
        user.customer.address_barangay = self.request.POST.get("address_barangay")
        user.customer.address_municipality = self.request.POST.get(
            "address_municipality"
        )
        user.customer.added_by = self.request.user.username
        user.save()
        messages.success(self.request, "Customer added successfully!!!")
        return redirect("doctors:customers_list_view")


def customer_profile_view(request):
    id = request.GET.get("id")
    customer_profile = customer_user.objects.get(id=id)
    pets_count = pets.objects.filter(owner_id=id).count()
    context = {"customer": customer_profile, "pets_count": pets_count}
    return render(request, "doctors/pages/customer_profile.html", context)


class staff_list_view(CheckGroupPermissionMixin, ListView):
    model = staff_user
    template_name = "doctors/pages/staff_list.html"
    paginate_by = 6

    def get_queryset(self):
        filter = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "auth_user_id_id")
        if filter != "":
            cat = staff_user.objects.filter(
                Q(first_name__contains=filter) | Q(last_name__contains=filter)
            ).order_by(order_by)
        else:
            cat = staff_user.objects.all().order_by(order_by)
        return cat

    def get_context_data(self, **kwargs):
        context = super(staff_list_view, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "auth_user_id_id")
        context["all_table_fields"] = staff_user._meta.get_fields()
        return context


class add_staff_view(CheckGroupPermissionMixin, SuccessMessageMixin, CreateView):
    model = custom_user
    template_name = "doctors/pages/add_staff.html"
    fields = ["first_name", "last_name", "email", "username", "password"]

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = 2
        user.set_password(form.cleaned_data["password"])
        user.save()

        profile_pic = self.request.FILES["profile_pic"]
        address_barangay = self.request.POST.get("address_barangay")
        address_municipality = self.request.POST.get("address_municipality")
        contact_number = self.request.POST.get("contact_number")
        user.staff.first_name = user.first_name
        user.staff.last_name = user.last_name
        user.staff.email = user.email
        user.staff.username = user.username
        user.staff.profile_pic = profile_pic
        user.staff.address_barangay = address_barangay
        user.staff.address_municipality = address_municipality
        user.staff.contact_number = contact_number
        user.staff.added_by = self.request.user.username
        user.save()
        messages.success(self.request, "Staff Added Successfully!!!")
        return redirect("doctors:staff_list_view")
        return super().form_valid(form)


def staff_profile_view(request):
    if request.user.is_authenticated and request.user.user_type == 1:
        context = None
        id = request.GET.get("id")
        staff_profile = staff_user.objects.get(auth_user_id=id)
        context = {"staff": staff_profile}
        return render(request, "doctors/pages/staff_profile.html", context)
    else:
        return redirect("/%s?next=%s" % ("doctors/login/", request.path))
