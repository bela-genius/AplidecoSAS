from django.db import models


class SiteSettings(models.Model):
    """Configuración global de marca (singleton)."""

    site_name = models.CharField(max_length=120, default="Aplideco S.A.S.")
    tagline = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    favicon = models.ImageField(upload_to="branding/", blank=True, null=True)
    hero_image = models.ImageField(
        upload_to="branding/",
        blank=True,
        null=True,
        help_text="Foto real de obra/proyecto para el hero del home (reemplaza el fondo de marcador de posición).",
    )
    primary_color = models.CharField(max_length=7, default="#1A1A1A")
    accent_color = models.CharField(max_length=7, default="#FF5A1F")
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    maps_url = models.URLField(
        blank=True,
        verbose_name="Enlace de Google Maps",
        help_text="Pega aquí el enlace de tu ficha de Google Maps (botón Compartir). Si queda vacío se busca por la dirección.",
    )

    years_experience = models.PositiveIntegerField(default=0)
    projects_completed = models.PositiveIntegerField(default=0)
    sqm_built = models.PositiveIntegerField(default=0, verbose_name="m² construidos/intervenidos")
    clients_satisfied = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Configuración del sitio"
        verbose_name_plural = "Configuración del sitio"

    def __str__(self) -> str:
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls) -> "SiteSettings":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SocialLink(models.Model):
    class Platform(models.TextChoices):
        INSTAGRAM = "instagram", "Instagram"
        FACEBOOK = "facebook", "Facebook"
        TIKTOK = "tiktok", "TikTok"
        WHATSAPP = "whatsapp", "WhatsApp"
        YOUTUBE = "youtube", "YouTube"
        LINKEDIN = "linkedin", "LinkedIn"
        X = "x", "X (Twitter)"

    platform = models.CharField(max_length=20, choices=Platform.choices, unique=True)
    url = models.URLField()
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.get_platform_display()}"


class Page(models.Model):
    """Páginas informativas: quiénes somos, contacto, etc."""

    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(max_length=250, blank=True)
    body = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to="pages/", blank=True, null=True)
    is_published = models.BooleanField(default=True)
    show_in_nav = models.BooleanField(default=True)
    nav_order = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nav_order", "title"]

    def __str__(self) -> str:
        return self.title


class Project(models.Model):
    """Proyecto de portafolio (obra ejecutada)."""

    class Category(models.TextChoices):
        RESIDENTIAL = "residencial", "Residencial"
        COMMERCIAL = "comercial", "Comercial"
        INDUSTRIAL = "industrial", "Industrial"

    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    location = models.CharField(max_length=150, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    sqm = models.PositiveIntegerField(null=True, blank=True, verbose_name="m² intervenidos")
    summary = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="projects/", blank=True, null=True)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-year"]

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify

            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class ContactRequest(models.Model):
    """Solicitud de contacto/cotización general (no ligada a un producto puntual)."""

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.full_name} ({self.created_at:%Y-%m-%d})"


class Appointment(models.Model):
    """Solicitud de cita (virtual o presencial) hecha desde la página Agenda tu cita."""

    class Modality(models.TextChoices):
        VIRTUAL = "virtual", "Virtual"
        IN_PERSON = "presencial", "Presencial"

    class Slot(models.TextChoices):
        MORNING = "manana", "Mañana"
        AFTERNOON = "tarde", "Tarde"

    class Status(models.TextChoices):
        PENDING = "pendiente", "Pendiente"
        CONFIRMED = "confirmada", "Confirmada"
        CANCELLED = "cancelada", "Cancelada"

    full_name = models.CharField("Nombre completo", max_length=150)
    phone = models.CharField("Teléfono / WhatsApp", max_length=30)
    email = models.EmailField("Correo electrónico", blank=True)
    modality = models.CharField("Modalidad", max_length=12, choices=Modality.choices, default=Modality.VIRTUAL)
    service = models.CharField("Servicio", max_length=40, blank=True)
    preferred_date = models.DateField("Fecha preferida", null=True, blank=True)
    preferred_slot = models.CharField("Franja preferida", max_length=10, choices=Slot.choices, default=Slot.MORNING)
    message = models.TextField("Cuéntanos qué necesitas", blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Cita"
        verbose_name_plural = "Citas"

    def __str__(self) -> str:
        when = f"{self.preferred_date:%Y-%m-%d}" if self.preferred_date else self.get_preferred_slot_display()
        return f"{self.full_name} · {self.get_modality_display()} · {when}"


class Certification(models.Model):
    """Certificación, sello o alianza institucional (calidad, sostenibilidad, etc.)."""

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=255, blank=True)
    badge = models.ImageField(upload_to="certifications/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return self.name
