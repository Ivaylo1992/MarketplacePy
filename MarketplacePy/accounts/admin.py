from django.contrib import admin
from django.contrib.auth import get_user_model

from MarketplacePy.accounts.forms import AppUserCreationForm, AppUserChangeForm
from MarketplacePy.accounts.models import AppUser

UserModel = get_user_model()


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    model = UserModel
    add_form = AppUserCreationForm
    form = AppUserChangeForm

    fieldsets = (
        (None, {"fields": ("email", "password",)}),
        ("Personal info", {"fields": ("first_name", "last_name",)}),
        ("Permissions", {
            "fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined",)}),
    )

    add_fieldsets = (
        (
            None, {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            }
        )
    )

    list_display = ("pk", "email", "is_staff", "is_superuser")

    search_fields = ("email", )

    ordering = ("pk",)