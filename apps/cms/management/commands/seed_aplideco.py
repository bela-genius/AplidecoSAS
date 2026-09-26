from django.core.management.base import BaseCommand

from apps.cms.models import Page, SiteSettings, SocialLink
from apps.store.models import Category, Product


class Command(BaseCommand):
    """Precarga datos reales/base de Aplideco S.A.S. (Medellín) y un catálogo de ejemplo.

    Los datos de contacto vienen de fuentes públicas (registro mercantil); el
    catálogo es de ejemplo y debe reemplazarse con la información real del cliente.
    """

    help = "Carga datos iniciales de marca y catálogo de ejemplo para Aplideco S.A.S."

    def handle(self, *args, **options):
        settings_obj = SiteSettings.load()
        settings_obj.site_name = "Aplideco S.A.S."
        settings_obj.tagline = "Acabados y remodelaciones de edificaciones en Medellín"
        settings_obj.contact_phone = "310 392 9839"
        settings_obj.address = "Calle 49 Cr 65 A 29, Medellín, Antioquia"
        settings_obj.primary_color = "#0F172A"
        settings_obj.accent_color = "#F59E0B"
        settings_obj.save()
        self.stdout.write(self.style.SUCCESS("SiteSettings actualizado."))

        SocialLink.objects.get_or_create(
            platform=SocialLink.Platform.FACEBOOK,
            defaults={"url": "https://www.facebook.com/aplideco/", "order": 1},
        )
        SocialLink.objects.get_or_create(
            platform=SocialLink.Platform.WHATSAPP,
            defaults={"url": "https://wa.me/573103929839", "order": 2},
        )
        self.stdout.write(self.style.SUCCESS("Redes sociales cargadas."))

        Page.objects.get_or_create(
            slug="quienes-somos",
            defaults={
                "title": "Quiénes somos",
                "subtitle": "Especialistas en acabados y terminación de edificaciones",
                "body": (
                    "Aplideco S.A.S. es una empresa de Medellín dedicada a la terminación y "
                    "acabado de edificaciones y obras de ingeniería civil: pisos, enchapes, "
                    "revestimientos y remodelaciones integrales.\n\n"
                    "Este contenido es un punto de partida — actualízalo con la historia, "
                    "misión y diferenciales reales de la empresa."
                ),
                "nav_order": 1,
            },
        )
        Page.objects.get_or_create(
            slug="contacto",
            defaults={
                "title": "Contacto",
                "subtitle": "Escríbenos y te ayudamos a cotizar tu proyecto",
                "body": "Calle 49 Cr 65 A 29, Medellín, Antioquia\nTeléfono: 310 392 9839",
                "nav_order": 2,
            },
        )
        self.stdout.write(self.style.SUCCESS("Páginas informativas creadas."))

        materiales, _ = Category.objects.get_or_create(name="Materiales de acabados", slug="materiales-acabados")
        servicios, _ = Category.objects.get_or_create(name="Servicios de remodelación", slug="servicios-remodelacion")

        demo_products = [
            dict(
                category=materiales,
                product_type=Product.ProductType.MATERIAL,
                name="Porcelanato rectificado 60x60 (ejemplo)",
                short_description="Acabado mate, ideal para pisos interiores.",
                price=68000,
                stock=250,
                is_featured=True,
            ),
            dict(
                category=materiales,
                product_type=Product.ProductType.MATERIAL,
                name="Pintura impermeabilizante para fachadas (ejemplo)",
                short_description="Galón, alta resistencia a la humedad.",
                price=95000,
                stock=80,
            ),
            dict(
                category=servicios,
                product_type=Product.ProductType.SERVICE,
                name="Enchape de baño completo (ejemplo)",
                short_description="Instalación de enchape en piso y paredes, incluye mano de obra.",
                price=1200000,
                price_is_estimate=True,
                stock=0,
                is_featured=True,
            ),
            dict(
                category=servicios,
                product_type=Product.ProductType.SERVICE,
                name="Pintura de fachada (ejemplo)",
                short_description="Aplicación de pintura exterior, precio según metraje.",
                price=450000,
                price_is_estimate=True,
                stock=0,
            ),
        ]
        for data in demo_products:
            Product.objects.get_or_create(name=data.pop("name"), defaults=data)

        self.stdout.write(self.style.SUCCESS("Catálogo de ejemplo creado. Reemplázalo con datos reales."))
