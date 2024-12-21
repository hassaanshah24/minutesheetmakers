from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_approval_chain, name="create_approval_chain"),
    path("list/", views.list_approval_chains, name="approval_chain_list"),
]
