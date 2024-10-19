from rest_framework import viewsets
from .models import Category, Book
from .serializers import CategorySerializer, BookSerializer
from rest_framework import generics


class CtegoryManage(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# class BookManage(viewsets.ModelViewSet):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer