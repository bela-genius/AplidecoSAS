from types import SimpleNamespace
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.store.models import Product

from .models import Page


class CanonicalSitemap(Sitemap):
    """Fuerza el dominio canónico (SITE_URL) sin importar por cuál host se consulte."""

    protocol = "https"

    def get_urls(self, page=1, site=None, protocol=None):
        host = urlparse(settings.SITE_URL).netloc
        return super().get_urls(page=page, site=SimpleNamespace(domain=host, name=host), protocol="https")


class StaticSitemap(CanonicalSitemap):
    changefreq = "monthly"

    def items(self):
        return ["cms:home", "cms:about", "cms:catalog", "cms:chatbot", "cms:schedule", "store:product_list", "cms:projects", "cms:contact"]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == "cms:home" else 0.8


class PageSitemap(CanonicalSitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Page.objects.filter(is_published=True)

    def location(self, obj):
        return reverse("cms:page_detail", args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at


class ProductSitemap(CanonicalSitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Product.objects.filter(is_active=True)

    def location(self, obj):
        return reverse("store:product_detail", args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at


sitemaps = {"static": StaticSitemap, "paginas": PageSitemap, "productos": ProductSitemap}
