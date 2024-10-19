from django.urls import path
from rest_framework import routers
from . import views

app_name = "book"
router = routers.DefaultRouter()
router.register(r"category", views.CtegoryManage, basename="category")
urlpatterns = []
urlpatterns = [
    path("", views.BookListCreateView.as_view(), name="book-list-create"),
    path(
        "<int:pk>/", views.BookRetrieveUpdateDestroyView.as_view(), name="book-detail"
    ),
]
urlpatterns += router.urls
