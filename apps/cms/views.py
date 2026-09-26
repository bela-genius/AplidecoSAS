from django.shortcuts import get_object_or_404, render

from apps.store.models import Product

from .models import Page


def home(request):
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    return render(request, "cms/home.html", {"featured_products": featured_products})


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, "cms/page_detail.html", {"page": page})
