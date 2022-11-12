from django.urls import path
from .views import index, list_table

urlpatterns = [
    path("", index, name="index"),
    path("list", list_table, name="list-table")
]
