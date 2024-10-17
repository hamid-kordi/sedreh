from django.contrib.auth.models import BaseUserManager
from rest_framework.response import Response
from rest_framework import status


class UserManagers(BaseUserManager):
    def create(self, username, email, password):
        if not email:
            raise ValueError("The Email field must be set.")
        if not username:
            raise ValueError("The Username field must be set.")
        if not password:
            raise ValueError("The Password field must be set.")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username=username, email=email, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
