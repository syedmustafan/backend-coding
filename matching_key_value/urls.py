from django.urls import path
from .views import ListTable, IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("list", ListTable.as_view(), name="list-table")
]
