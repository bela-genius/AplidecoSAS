import json

from django.conf import settings
from django.templatetags.static import static

from .models import Page, SiteSettings, SocialLink


def _organization_jsonld(site, socials):
    data = {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "name": site.site_name,
        "url": settings.SITE_URL + "/",
        "logo": settings.SITE_URL + static("img/emblem-red.png"),
        "image": settings.SITE_URL + static("img/og-image.jpg"),
        "description": (
            "Pintura de fachadas, estucos, impermeabilización, acabados decorativos "
            "y obras civiles en Medellín y el Valle de Aburrá."
        ),
        "areaServed": {"@type": "City", "name": "Medellín"},
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Medellín",
            "addressRegion": "Antioquia",
            "addressCountry": "CO",
        },
    }
    if site.address:
        data["address"]["streetAddress"] = site.address
    digits = "".join(ch for ch in (site.whatsapp_number or site.contact_phone) if ch.isdigit())
    if digits:
        data["telephone"] = "+" + (digits if digits.startswith("57") else "57" + digits)
    if site.contact_email:
        data["email"] = site.contact_email
    links = [link.url for link in socials if link.platform != "whatsapp"]
    if site.maps_url:
        links.append(site.maps_url)
    if links:
        data["sameAs"] = links
    return json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")


def site_settings(request):
    site = SiteSettings.load()
    socials = list(SocialLink.objects.filter(is_active=True))
    return {
        "site_settings": site,
        "social_links": socials,
        "nav_pages": Page.objects.filter(is_published=True, show_in_nav=True),
        "site_url": settings.SITE_URL,
        "google_site_verification": settings.GOOGLE_SITE_VERIFICATION,
        "organization_jsonld": _organization_jsonld(site, socials),
    }
