from django.db import models


class SiteSettings(models.Model):
    """Configuración global de marca (singleton)."""

    site_name = models.CharField(max_length=120, default="Aplideco S.A.S.")
    tagline = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    favicon = models.ImageField(upload_to="branding/", blank=True, null=True)
    primary_color = models.CharField(max_length=7, default="#0F172A")
    accent_color = models.CharField(max_length=7, default="#22D3EE")
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)

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
