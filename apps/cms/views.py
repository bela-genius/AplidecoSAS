from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from apps.store.models import Category, Product

from .forms import SERVICES, AppointmentForm
from .models import Appointment, Certification, ContactRequest, Page, Project, SiteSettings


CYL_VERBS = ["Diseña", "Crea", "Imagina", "Construye", "Renueva"]
CYL_NOUNS = ["fachadas", "pinturas", "trabajos", "obras", "decoraciones"]


def _drum(words):
    return [{"w": word, "a": i * 72, "k": i} for i, word in enumerate(words)]


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
        "verbs": _drum(CYL_VERBS),
        "nouns": _drum(CYL_NOUNS),
    }
    return render(request, "cms/home.html", context)


LEGAL_DATA = [
    ("Razón social", "Aplideco S.A.S"),
    ("Tipo de sociedad", "Sociedad por Acciones Simplificada"),
    ("NIT", "901.079.715-6"),
    ("Domicilio", "Medellín, Antioquia"),
    ("Matrícula mercantil", "Activa · Registro RUES"),
]

WORK_FIELDS = [
    {
        "kicker": "Acabados",
        "title": "Terminación y acabado de edificios y obras de ingeniería civil",
        "chips": [
            "Pintura de interiores y exteriores",
            "Enlucido y estuco",
            "Yeso y paneles en seco",
            "Revestimientos",
            "Vidriería",
        ],
    },
    {
        "kicker": "Instalaciones",
        "title": "Otras instalaciones especializadas",
        "chips": ["Aislamiento", "Sellado de filtraciones", "Impermeabilización"],
    },
]


def about(request):
    return render(request, "cms/about.html", {"legal": LEGAL_DATA, "work": WORK_FIELDS})


CATALOG_SLIDES = [
    {"img": "tower", "alt": "Operario con casco trabajando en altura en una torre", "pos": "50% 50%", "cap": "Trabajo en alturas", "desc": "Intervenciones en fachadas y estructuras elevadas."},
    {"img": "stone", "alt": "Muro de piedra texturizada con luces puntuales", "pos": "50% 50%", "cap": "Muro texturizado", "desc": "Acabados con textura y carácter para interiores."},
    {"img": "facade", "alt": "Operarios pintando una fachada colgados de cuerdas", "pos": "50% 35%", "cap": "Pintura de fachada", "desc": "Pintura y protección de fachadas de edificios."},
    {"img": "scaffold", "alt": "Operario sobre un andamio en el acceso de un local", "pos": "50% 40%", "cap": "Obra en acceso", "desc": "Adecuaciones de accesos y frentes comerciales."},
]


def catalog(request):
    return render(request, "cms/catalog.html", {"slides": CATALOG_SLIDES})


CHATBOT_CHIPS = ["Cotizar pintura de fachada", "Impermeabilizar mi terraza", "Agendar una visita técnica", "Conocer servicios"]


def chatbot(request):
    return render(request, "cms/chatbot.html", {"chips": CHATBOT_CHIPS})


def page_detail(request, slug):
    if slug == "quienes-somos":
        return redirect("cms:about", permanent=True)
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


def appointment_message(appointment):
    lines = [
        "Hola Aplideco, quiero agendar una cita.",
        f"Modalidad: {appointment.get_modality_display()}",
        f"Nombre: {appointment.full_name}",
        f"Teléfono: {appointment.phone}",
        f"Servicio: {appointment.service}",
    ]
    slot = appointment.get_preferred_slot_display()
    if appointment.preferred_date:
        lines.append(f"Fecha preferida: {appointment.preferred_date:%d/%m/%Y} ({slot})")
    else:
        lines.append(f"Jornada preferida: {slot}")
    return "\n".join(lines)


def schedule(request):
    initial_modality = request.GET.get("modalidad")
    if initial_modality not in Appointment.Modality.values:
        initial_modality = Appointment.Modality.VIRTUAL

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            request.session["last_appointment"] = appointment.pk
            return redirect(f"{request.path}?enviado=1")
    else:
        form = AppointmentForm(initial={"modality": initial_modality, "preferred_slot": Appointment.Slot.MORNING})

    appointment = None
    wa_url = ""
    if request.GET.get("enviado") and request.session.get("last_appointment"):
        appointment = Appointment.objects.filter(pk=request.session["last_appointment"]).first()
        if appointment:
            from urllib.parse import quote

            number = SiteSettings.load().whatsapp_number or "573103929839"
            wa_url = f"https://wa.me/{number}?text={quote(appointment_message(appointment))}"
    return render(
        request,
        "cms/schedule.html",
        {"form": form, "appointment": appointment, "wa_url": wa_url, "services": SERVICES},
    )
