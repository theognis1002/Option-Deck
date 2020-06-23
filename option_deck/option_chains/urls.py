from django.urls import path
from .views import (
    ChainListView, 
    ChainDetailView, 
    ChainCreateView,
    ChainUpdateView,
    ChainDeleteView
    )
from . import views

urlpatterns = [
    path('', ChainListView.as_view(), name='home'),
    path('chain/<int:pk>/', ChainDetailView.as_view(), name='chain-detail'),
    path('chain/new/', ChainCreateView.as_view(), name='chain-create'),
    path('chain/<int:pk>/update/', ChainUpdateView.as_view(), name='chain-update'),
    path('chain/<int:pk>/delete/', ChainDeleteView.as_view(), name='chain-delete'),

    path('faq', views.faq, name='faq'),
    path('about', views.about, name='about'),
]