from .models import Page, SiteSettings, SocialLink


def site_settings(request):
    return {
        "site_settings": SiteSettings.load(),
        "social_links": SocialLink.objects.filter(is_active=True),
        "nav_pages": Page.objects.filter(is_published=True, show_in_nav=True),
    }
