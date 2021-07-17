from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


# Create your views here.

class isUserLogin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if (not self.request.user.is_authenticated):
            return redirect("doctors:doctors_login_view")
        if (not self.request.user.user_type == 1):
            return redirect("doctors:doctors_login_view")
        return super(isUserLogin, self).dispatch(request, *args, **kwargs)


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
    return render(request, "doctors/pages/doctors_dashboard.html", {})
