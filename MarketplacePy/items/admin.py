from django.contrib import admin

from MarketplacePy.items.models import Category, Item, ItemPhoto


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "pk")
    search_fields = ("name",)
    ordering = ("pk",)
    list_filter = ("created_at",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at", "pk")
    search_fields = ("name",)
    ordering = ("-created_at",)
    list_filter = ("created_at",)


@admin.register(ItemPhoto)
class ItemPhotoAdmin(admin.ModelAdmin):
    list_display = ("created_at", "updated_at", "pk")
    ordering = ("-created_at",)
    list_filter = ("created_at",)

