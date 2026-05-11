from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


def landing(request):
    return render(request, "landing.html")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
