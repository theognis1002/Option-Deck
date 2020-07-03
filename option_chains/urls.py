from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
from .views import (ChainCreateView, ChainDeleteView, ChainDetailView,
                    ChainListView, ChainUpdateView)

urlpatterns = [
    path("", login_required(ChainListView.as_view()), name="home"),
    path("treasury_rates", login_required(views.interest_rates), name="interest_rates"),
    path(
        "chain/<int:pk>/",
        login_required(ChainDetailView.as_view()),
        name="chain-detail",
    ),
    path("chain/new/", login_required(ChainCreateView.as_view()), name="chain-create"),
    path(
        "chain/<int:pk>/update/",
        login_required(ChainUpdateView.as_view()),
        name="chain-update",
    ),
    path(
        "chain/<int:pk>/delete/",
        login_required(ChainDeleteView.as_view()),
        name="chain-delete",
    ),
    path("faq", views.faq, name="faq"),
    path("about", views.about, name="about"),
]
