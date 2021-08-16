from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
from accounts.models import (
    customer as customer_user,
    Admin as admin_user,
    User as custom_user,
    staff as staff_user,
)
from pets.models import pets as customer_pets
from blogs.models import Blogs as doctors_blogs

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
            doctors = admin_user.objects.all().count()
            staff = staff_user.objects.all().count()
            customer = customer_user.objects.all().count()
            pets = customer_pets.objects.all().count()
            context = {
                "doctors": doctors,
                "staff": staff,
                "customer": customer,
                "pets": pets,
            }
            return render(request, "doctors/pages/doctors_dashboard.html", context)
        else:
            return redirect("doctors:doctors_login_view")
    else:
        return redirect("/%s?next=%s" % ("doctors/login/", request.path))
        # return HttpResponseRedirect("doctors:doctors_login_view")


def doctors_logout_view(request):
    logout(request)
    return redirect("doctors:doctors_login_view")


class pets_list_view(CheckGroupPermissionMixin, ListView):
    model = customer_pets
    template_name = "doctors/pages/pets_list.html"
    paginate_by = 6

    def get_queryset(self):
        filter = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "id")
        if filter != "":
            if filter.isnumeric():
                cat = customer_pets.objects.filter(owner_id=filter).order_by(order_by)
            else:
                cat = customer_pets.objects.filter(
                    Q(pet_name__contains=filter)
                    | Q(breed__contains=filter)
                    | Q(owner__contains=filter)
                ).order_by(order_by)
        else:
            cat = customer_pets.objects.all().order_by(order_by)
        return cat

    def get_context_data(self, **kwargs):
        context = super(pets_list_view, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "id")
        context["all_table_fields"] = customer_pets._meta.get_fields()
        return context


class add_pet_view(CheckGroupPermissionMixin, CreateView):
    model = customer_pets
    template_name = "doctors/pages/add_pet.html"
    fields = ["pet_image", "pet_name", "breed", "age", "owner", "added_by", "owner_id"]

    def form_valid(self, form):
        pets_id = customer_pets.objects.all()
        max = 0
        for id in pets_id:
            if id.id > max:
                max = id.id
        pet = form.save(commit=False)
        pet.id = max + 1
        pet.save()
        return redirect("doctors:pets_list_view")


class add_pet_specific_customer_view(CheckGroupPermissionMixin, CreateView):
    model = customer_pets
    template_name = "doctors/pages/add_pet_specific_customer.html"
    fields = ["pet_image", "pet_name", "breed", "age", "owner", "added_by"]

    def form_valid(self, form):
        pets_id = customer_pets.objects.all()
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
    model = customer_pets
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

        user.customer.username = user.username
        user.customer.first_name = user.first_name
        user.customer.last_name = user.last_name
        user.customer.email = user.email
        user.customer.profile_pic = self.request.FILES["profile_pic"]
        user.customer.contact_number = self.request.POST.get("contact_number")
        user.customer.address_barangay = self.request.POST.get("address_barangay")
        user.customer.address_municipality = self.request.POST.get(
            "address_municipality"
        )
        user.customer.added_by = self.request.user.email
        user.save()
        messages.success(self.request, "Customer added successfully!!!")
        return redirect("doctors:customers_list_view")


def customer_profile_view(request):
    id = request.GET.get("id")
    customer_profile = customer_user.objects.get(id=id)
    pets_count = customer_pets.objects.filter(owner_id=id).count()
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

        user.staff.username = user.username
        user.staff.first_name = user.first_name
        user.staff.last_name = user.last_name
        user.staff.email = user.email
        user.staff.profile_pic = profile_pic
        user.staff.address_barangay = address_barangay
        user.staff.address_municipality = address_municipality
        user.staff.contact_number = contact_number
        user.staff.added_by = self.request.user.email
        user.save()
        messages.success(self.request, "Staff Added Successfully!!!")
        return redirect("doctors:staff_list_view")


def staff_profile_view(request):
    if request.user.is_authenticated and request.user.user_type == 1:
        context = None
        id = request.GET.get("id")
        staff_profile = staff_user.objects.get(auth_user_id=id)
        context = {"staff": staff_profile}
        return render(request, "doctors/pages/staff_profile.html", context)
    else:
        return redirect("/%s?next=%s" % ("doctors/login/", request.path))


class add_doctor_view(CheckGroupPermissionMixin, SuccessMessageMixin, CreateView):
    model = custom_user
    template_name = "doctors/pages/add_doctor.html"
    fields = ["first_name", "last_name", "email", "username", "password"]

    def form_valid(self, form):
        doctor = form.save(commit=False)
        doctor.user_type = 1
        doctor.set_password(form.cleaned_data["password"])
        doctor.save()
        doctor.admin.profile_pic = self.request.FILES["profile_pic"]
        doctor.admin.contact_number = self.request.POST.get("contact_number")
        doctor.admin.address_barangay = self.request.POST.get("address_barangay")
        doctor.admin.address_municipality = self.request.POST.get(
            "address_municipality"
        )
        doctor.admin.added_by = None
        doctor.save()

        return redirect("doctors:add_doctor_view")


class doctors_list_view(CheckGroupPermissionMixin, ListView):
    model = custom_user
    template_name = "doctors/pages/doctors_list.html"
    paginate_by = 6

    def get_queryset(self):
        filter = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "id")
        if filter != "":
            cat = custom_user.objects.filter(
                Q(first_name__contains=filter)
                | Q(last_name__contains=filter) & Q(user_type=1)
            ).order_by(order_by)
        else:
            cat = custom_user.objects.filter(user_type=1).order_by(order_by)
        return cat

    def get_context_data(self, **kwargs):
        context = super(doctors_list_view, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby")
        context["all_table_fields"] = custom_user._meta.get_fields()
        return context


def doctors_profile_view(request):
    context = None
    if request.user.is_authenticated and request.user.user_type == 1:
        id = request.GET.get("id")
        if id is not None:
            doctor = custom_user.objects.get(id=id)
            context = {"doctor": doctor}
            return render(request, "doctors/pages/doctors_profile.html", context)
        else:
            return HttpResponse("Missing parameter")

    else:
        return redirect("doctors:doctors_login_view")


def send_email_view(request):
    if request.method == "POST":
        recipient = request.POST.get("recipient")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            recipient,
        ]
        send_mail(subject, message, email_from, recipient_list)
        return HttpResponse("Sent")


def password_reset_view(request):
    return render(request, "doctors/auth/password_reset.html", {})


def validate_email_for_doctors_password_reset(request):
    if request.method == "POST":
        email = request.POST.get("new_email")
        user = custom_user.objects.filter(email=email).count()
        if user == 1:
            return HttpResponse("1")
        else:
            return HttpResponse("0")


def send_otp_via_email_view(request):
    if request.method == "POST":
        recipient = request.POST.get("user_email")
        subject = "Your OTP"
        message = request.POST.get("new_otp")
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            recipient,
        ]
        send_mail(subject, message, email_from, recipient_list)
        return HttpResponse("Sent")


def doctors_password_reset_view(request):
    if request.method == "POST":
        email = request.POST.get("confirm_email")
        new_password = request.POST.get("new_password")
        user = custom_user.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return HttpResponse("Password updated successfully")


class account_update_view(CheckGroupPermissionMixin, SuccessMessageMixin, UpdateView):
    model = custom_user
    template_name = "doctors/pages/account_update.html"
    fields = ["first_name", "last_name", "email", "username", "password"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = admin_user.objects.get(auth_user_id=self.object.pk)
        context["account"] = model
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()

        admin = admin_user.objects.get(auth_user_id=user.id)
        if self.request.FILES.get("profile_pic", False):
            admin.profile_pic = self.request.FILES["profile_pic"]
        admin.contact_number = self.request.POST.get("contact_number")
        admin.address_barangay = self.request.POST.get("address_barangay")
        admin.address_municipality = self.request.POST.get("address_municipality")
        admin.save()
        return redirect("doctors:doctors_login_view")


class add_blog_view(CheckGroupPermissionMixin, CreateView):
    model = doctors_blogs
    template_name = "doctors/pages/add_blogs.html"
    fields = [
        "illness_image",
        "illness_name",
        "illness_description",
        "illness_prevention",
    ]

    def form_valid(self, form):
        max = 0
        blogs = doctors_blogs.objects.all()
        for blog in blogs:
            if blog.id > max:
                max = blog.id
        new_blog = form.save(commit=False)
        new_blog.id = max + 1
        new_blog.illness_uploader = self.request.user
        new_blog.save()
        return redirect("doctors:add_blog_view")


class blog_list_view(CheckGroupPermissionMixin, ListView):
    model = doctors_blogs
    template_name = "doctors/pages/blog_list.html"
    paginate_by = 2
