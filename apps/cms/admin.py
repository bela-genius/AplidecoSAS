from django.contrib import admin

from .models import Page, SiteSettings, SocialLink


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "is_active", "order")
    list_editable = ("is_active", "order")


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "is_published", "show_in_nav", "nav_order", "updated_at")
    list_editable = ("is_published", "show_in_nav", "nav_order")
