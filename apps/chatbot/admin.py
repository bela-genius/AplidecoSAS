from django.contrib import admin

from .models import Conversation, KnowledgeEntry, Message


@admin.register(KnowledgeEntry)
class KnowledgeEntryAdmin(admin.ModelAdmin):
    list_display = ("question_example", "trigger_keywords", "priority", "is_active")
    list_editable = ("priority", "is_active")


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ("sender", "text", "created_at")


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "session_key", "created_at")
    inlines = [MessageInline]
