from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, AbstractUser
from .managers import UserManagers
from django.utils import timezone
from book.models import Book
from tasks import celery_increaseـtheـbudget, celery_buy_book, celery_return_book

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True, blank=False, null=True)
    budget = models.IntegerField(default=0)
    objects = UserManagers()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def increaseـtheـbudget(self, user_id, code):
        if user_id and code:
            task = celery_increaseـtheـbudget.delay(user_id, code)
        else:
            raise ValueError("user_id and code is necessary")

    def buy_book(self, user_id, book_id):
        if user_id and book_id:
            task = celery_buy_book.delay(user_id, book_id)
        else:
            raise ValueError("user_id and book_id is necessary")

    def return_the_book(self, user_id, book_id):
        if user_id and book_id:
            task = celery_return_book(user_id, book_id)
        else:
            raise ValueError("user_id and book_id is necessary")


class OtpCode(models.Model):
    email = models.EmailField(max_length=11, unique=True)
    code = models.PositiveSmallIntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    price = models.IntegerField(default=0, null=False, blank=True)
    expiration_date = models.DateTimeField(default=timezone)

    def __str__(self):
        return f"{self.email} - {self.code} - {self.created}"


class Library(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
