from django.contrib import admin

from .models import Certification, ContactRequest, Page, Project, SiteSettings, SocialLink


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


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "category", "location", "year", "is_published", "is_featured", "order")
    list_editable = ("is_published", "is_featured", "order")
    list_filter = ("category", "is_published")


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "is_handled", "created_at")
    list_editable = ("is_handled",)
    list_filter = ("is_handled",)
    readonly_fields = ("full_name", "email", "phone", "message", "created_at")
