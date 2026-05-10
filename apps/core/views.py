from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def landing(request):
    return render(request, "landing.html")


@login_required
def dashboard(request):
    return render(request, "dashboard.html")
