from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
    )
from .models import Chain


def home(request):
    context = {
        'chains': Chain.objects.all(),
        'title': 'Home'
    }
    return render(request, 'option_chains/home.html', context)


def faq(request):
    context = {
        'title': 'FAQ'
    }
    return render(request, 'option_chains/faq.html', context)


def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'option_chains/about.html', context)


class ChainListView(ListView):
    model = Chain
    template_name = 'option_chains/home.html'
    context_object_name = 'chains'
    ordering = ['-date_updated']
    paginate_by = 2



class ChainDetailView(DetailView):
    model = Chain
    

class ChainCreateView(CreateView):
    model = Chain
    fields = ['ticker', 'company_name', 'description', 'price', 'pe']


class ChainUpdateView(LoginRequiredMixin, UpdateView):
    model = Chain
    fields = ['ticker', 'company_name', 'description', 'price', 'pe']


class ChainDeleteView(LoginRequiredMixin, DeleteView):
    model = Chain
    success_url = '/'