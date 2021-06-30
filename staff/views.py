from django.shortcuts import render, redirect


from pets.forms import pets_form
# Create your views here.


def staff_dashboard_view(request):
    # if request.method == 'POST':
    form = pets_form()
    # if form.is_valid():

    return render(request, "staff/staff_dashboard.html", {'form': form})
