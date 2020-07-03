from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Chain
from .options import treasury_rates


@login_required
def home(request):
    context = {"chains": Chain.objects.all(), "title": "Home"}
    return render(request, "option_chains/home.html", context)


@login_required
def interest_rates(request):
    rates = treasury_rates()
    context = {"rates": rates}
    return render(request, "option_chains/interest_rates.html", context)


@login_required
def faq(request):
    context = {"title": "FAQ"}
    return render(request, "option_chains/faq.html", context)


def about(request):
    context = {"title": "About"}
    return render(request, "option_chains/about.html", context)


class ChainListView(ListView):
    model = Chain
    template_name = "option_chains/home.html"
    context_object_name = "chains"
    ordering = ["-date_updated"]
    paginate_by = 5


class ChainDetailView(DetailView):
    model = Chain


class ChainCreateView(CreateView):
    model = Chain
    fields = ["ticker", "company_name", "description", "price", "pe"]


class ChainUpdateView(LoginRequiredMixin, UpdateView):
    model = Chain
    fields = ["ticker", "company_name", "description", "price", "pe"]


class ChainDeleteView(LoginRequiredMixin, DeleteView):
    model = Chain
    success_url = "/"
