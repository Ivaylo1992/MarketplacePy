from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'get_members', 'updated_at', 'created_at')
    search_fields = ('item__name',  'members__email')
    list_filter = ('updated_at', 'created_at')

    def get_members(self, obj):
        return ", ".join([member.email for member in obj.members.all()])
    get_members.short_description = "Members"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'user', 'content_snippet', 'created_at', 'updated_at')
    search_fields = ('conversation__item__name', 'user__email', 'content')
    list_filter = ('created_at', 'updated_at')

    def content_snippet(self, obj):
        return obj.content[:50] + "..." if obj.content and len(obj.content) > 50 else obj.content
    content_snippet.short_description = "Content Snippet"