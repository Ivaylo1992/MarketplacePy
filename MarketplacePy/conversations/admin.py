from django.contrib import admin

from MarketplacePy.conversations.models import Conversation


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("pk", "get_members", "item")
    search_fields = ("pk", "item__name")

    def get_members(self, obj):
        return ", ".join([str(member) for member in obj.members.all()])

    get_members.short_description = "Members"
