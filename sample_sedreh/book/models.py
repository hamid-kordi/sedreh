from django.db import models
from django.urls import reverse

# from ckeditor.fields import RichTextField
# Create your models here.


class Category(models.Model):
    sub_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="scategory",
        null=True,
        blank=True,
    )
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "my_cetegory"
        verbose_name_plural = "my_cetegories"

    def __str__(self):
        return self.name


class Book(models.Model):
    category = models.ManyToManyField(Category, related_name="books")
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to="book_files/", blank=True, null=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name
