from django.urls import path
from .views import index, list_table

urlpatterns = [
    path("", index, name="index"),
    path("new", list_table, name="list-table")
]