from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.db.models import Q

from accounts.models import customer
from pets.models import pets


# Create your views here.

class CheckGroupPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="doctors_group"):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("doctors:doctors_login_view")


def doctors_login_view(request):
    status = None
    context = None
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.user_type == 1:
                    login(request, user)
                    if request.GET.get('next'):
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect("doctors:doctors_dashboard_view")
                else:
                    status = "Invalid Account!!!"
        else:
            status = form.errors
            form = AuthenticationForm()
    context = {
        'status': status,
        'form': form
    }
    return render(request, "doctors/auth/login.html", context)


def doctors_dashboard_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return render(request, "doctors/pages/doctors_dashboard.html", {})
        else:
            return redirect("doctors:doctors_login_view")
    else:
        return redirect("doctors:doctors_login_view")


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


class add_pet_view(CheckGroupPermissionMixin, CreateView):
    model = pets
    template_name = "doctors/pages/add_pet.html"
    fields = "__all__"

    def form_valid(self, form):
        form.save()
        return redirect("doctors:pets_list_view")
