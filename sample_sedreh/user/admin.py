from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


# Register your models here.
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "email", "username", "budget", "is_active")
    list_filter = ("budget",)
    readonly_fields = ("last_login",)
    fieldsets = (
        ("Main", {"fields": ("email", "username", "password", "budget", "is_active")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "budget",
                    "email",
                    "password1",
                    "password2",
                )
            },
        ),
    )

    search_fields = ("email", "username")


admin.site.register(User, UserAdmin)
