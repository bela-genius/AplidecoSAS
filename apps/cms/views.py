from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from apps.store.models import Category, Product

from .models import Certification, ContactRequest, Page, Project, SiteSettings


def home(request):
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:4]
    service_categories = Category.objects.filter(is_active=True, show_as_service=True)
    featured_projects = Project.objects.filter(is_published=True, is_featured=True)[:3]
    slider_projects = Project.objects.filter(is_published=True)[:7]
    certifications = Certification.objects.all()
    settings_obj = SiteSettings.load()
    trust_stats = [
        {
            "icon": "partials/icons/calendar.svg",
            "value": settings_obj.years_experience,
            "label": "Años de experiencia",
        },
        {
            "icon": "partials/icons/building.svg",
            "value": settings_obj.projects_completed,
            "label": "Proyectos ejecutados",
        },
        {
            "icon": "partials/icons/ruler.svg",
            "value": settings_obj.sqm_built,
            "label": "m² intervenidos",
        },
        {
            "icon": "partials/icons/users.svg",
            "value": settings_obj.clients_satisfied,
            "label": "Clientes satisfechos",
        },
    ]
    context = {
        "featured_products": featured_products,
        "service_categories": service_categories,
        "featured_projects": featured_projects,
        "slider_projects": slider_projects,
        "certifications": certifications,
        "trust_stats": trust_stats,
    }
    return render(request, "cms/home.html", context)


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    certifications = Certification.objects.all()
    return render(request, "cms/page_detail.html", {"page": page, "certifications": certifications})


def project_list(request):
    projects = Project.objects.filter(is_published=True)
    category = request.GET.get("categoria")
    if category:
        projects = projects.filter(category=category)
    context = {
        "projects": projects,
        "categories": Project.Category.choices,
        "selected_category": category,
    }
    return render(request, "cms/project_list.html", context)


def contact(request):
    if request.method == "POST":
        ContactRequest.objects.create(
            full_name=request.POST.get("full_name", ""),
            email=request.POST.get("email", ""),
            phone=request.POST.get("phone", ""),
            message=request.POST.get("message", ""),
        )
        messages.success(request, "Recibimos tu solicitud. Te contactaremos muy pronto.")
        return redirect("cms:contact")
    return render(request, "cms/contact.html")
