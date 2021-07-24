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

from accounts.models import customer as customer_user, User as custom_user
from pets.models import pets


# Create your views here.


class CheckGroupPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="doctors_group"):
            return super().dispatch(request, *args, **kwargs)
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
    fields = "__all__"

    def form_valid(self, form):
        form.save()
        return redirect("doctors:pets_list_view")


class update_pet(CheckGroupPermissionMixin, UpdateView):
    model = pets
    template_name = "doctors/pages/pet_update.html"
    success_message = "Pet Updated Successfully!!!"
    fields = "__all__"

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
