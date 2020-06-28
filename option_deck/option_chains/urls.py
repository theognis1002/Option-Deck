from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    ChainListView, 
    ChainDetailView, 
    ChainCreateView,
    ChainUpdateView,
    ChainDeleteView
    )
from . import views

urlpatterns = [
    path('', login_required(ChainListView.as_view()), name='home'),
    path('chain/<int:pk>/', login_required(ChainDetailView.as_view()), name='chain-detail'),
    path('chain/new/', login_required(ChainCreateView.as_view()), name='chain-create'),
    path('chain/<int:pk>/update/', login_required(ChainUpdateView.as_view()), name='chain-update'),
    path('chain/<int:pk>/delete/', login_required(ChainDeleteView.as_view()), name='chain-delete'),
    path('faq', views.faq, name='faq'),
    path('about', views.about, name='about'),
]