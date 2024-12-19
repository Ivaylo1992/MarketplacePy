from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from MarketplacePy.accounts.forms import AppUserCreationForm, AppUserChangeForm
from MarketplacePy.accounts.models import AppUser, Profile, UserReview

UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(UserAdmin):
    model = UserModel
    add_form = AppUserCreationForm
    form = AppUserChangeForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),  # Remove this if you have no personal info fields.
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            None, {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            }
        ),
    )

    list_display = ("pk", "email", "is_staff", "is_superuser")

    search_fields = ("email",)

    ordering = ("pk",)

    readonly_fields = ("last_login", "date_joined")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_name', 'location')

    search_fields = ('user__username', 'user__email', 'first_name', 'last_name', 'location')

    list_filter = ('location',)


@admin.register(UserReview)
class UserReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'reviewed_user', 'rating', 'created_at', 'comment_snippet')
    search_fields = ('reviewer__username', 'reviewer__email', 'reviewed_user__username', 'reviewed_user__email')
    list_filter = ('rating', 'created_at')

    def comment_snippet(self, obj):
        return obj.comment[:50] + "..." if obj.comment and len(obj.comment) > 50 else obj.comment

    comment_snippet.short_description = "Comment Snippet"
