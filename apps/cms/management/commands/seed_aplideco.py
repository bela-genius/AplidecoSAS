from django.core.management.base import BaseCommand

from apps.cms.models import Certification, Page, Project, SiteSettings, SocialLink
from apps.store.models import Category, Product


class Command(BaseCommand):
    """Precarga datos reales/base de Aplideco S.A.S. (Medellín) y un catálogo de ejemplo.

    Los datos de contacto vienen de fuentes públicas (registro mercantil); el
    catálogo, proyectos y cifras son de ejemplo y deben reemplazarse con la
    información real del cliente.
    """

    help = "Carga datos iniciales de marca y catálogo de ejemplo para Aplideco S.A.S."

    def handle(self, *args, **options):
        settings_obj = SiteSettings.load()
        settings_obj.site_name = "Aplideco S.A.S."
        settings_obj.tagline = "Construimos con identidad."
        settings_obj.contact_phone = "310 392 9839"
        settings_obj.whatsapp_number = "573103929839"
        settings_obj.address = "Calle 49 Cr 65 A 29, Medellín, Antioquia"
        # Paleta institucional — Manual de Identidad Corporativa APLIDECO S.A.S.
        settings_obj.primary_color = "#000000"  # Obsidian
        settings_obj.accent_color = "#ED1C24"  # Alarm Red
        settings_obj.years_experience = 12
        settings_obj.projects_completed = 180
        settings_obj.sqm_built = 45000
        settings_obj.clients_satisfied = 140
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
                "subtitle": "Aplicaciones · Decoraciones y Obras Civiles",
                "body": (
                    "APLIDECO S.A.S. es una empresa colombiana que aplica acabados, decora "
                    "espacios y ejecuta obras civiles, con la seguridad y la calidad como "
                    "base de cada proyecto.\n\n"
                    "Aplicaciones: pintura, estucos, impermeabilizaciones y recubrimientos "
                    "en interiores y fachadas.\n"
                    "Decoraciones: acabados y detalles que transforman espacios "
                    "residenciales y comerciales.\n"
                    "Obras civiles: construcción, adecuación y mantenimiento de "
                    "infraestructura.\n\n"
                    "Nuestros valores: Seguridad, Calidad, Cumplimiento, Responsabilidad y "
                    "Trabajo en equipo.\n\n"
                    "Sostenibilidad (ejemplo): priorizamos materiales de bajo impacto y "
                    "procesos que reducen el desperdicio de obra. Reemplazar con la política "
                    "real de sostenibilidad de la empresa."
                ),
                "nav_order": 1,
            },
        )
        self.stdout.write(self.style.SUCCESS("Páginas informativas creadas."))

        Certification.objects.get_or_create(
            name="Afiliados Cámara de Comercio de Medellín (ejemplo)",
            defaults={"description": "Reemplazar con certificaciones/sellos reales.", "order": 1},
        )
        Certification.objects.get_or_create(
            name="Compromiso con obra segura (ejemplo)",
            defaults={"description": "Reemplazar con certificaciones/sellos reales.", "order": 2},
        )

        categories_data = [
            dict(name="Pisos", slug="pisos", icon=Category.Icon.FLOOR, short_pitch="Instalación y suministro de pisos técnicos y decorativos.", order=1),
            dict(name="Enchapes", slug="enchapes", icon=Category.Icon.TILE, short_pitch="Enchape de baños, cocinas y fachadas con acabado de precisión.", order=2),
            dict(name="Pintura", slug="pintura", icon=Category.Icon.PAINT, short_pitch="Pintura interior, exterior e impermeabilizante para fachadas.", order=3),
            dict(name="Remodelaciones", slug="remodelaciones", icon=Category.Icon.REMODEL, short_pitch="Remodelación integral de espacios residenciales y comerciales.", order=4),
        ]
        categories = {}
        for data in categories_data:
            slug = data.pop("slug")
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={**data, "name": data["name"]})
            categories[slug] = cat
        self.stdout.write(self.style.SUCCESS("Categorías/servicios creados."))

        demo_products = [
            dict(
                category=categories["pisos"],
                product_type=Product.ProductType.MATERIAL,
                name="Porcelanato rectificado 60x60 (ejemplo)",
                short_description="Acabado mate, ideal para pisos interiores.",
                price=68000,
                unit="m²",
                stock=250,
                is_featured=True,
                specs={"Formato": "60x60 cm", "Resistencia": "PEI 4", "Acabado": "Mate rectificado"},
            ),
            dict(
                category=categories["pintura"],
                product_type=Product.ProductType.MATERIAL,
                name="Pintura impermeabilizante para fachadas (ejemplo)",
                short_description="Galón, alta resistencia a la humedad.",
                price=95000,
                unit="galón",
                stock=80,
                specs={"Rendimiento": "10 m²/galón", "Secado": "4 horas", "Base": "Acrílica"},
            ),
            dict(
                category=categories["enchapes"],
                product_type=Product.ProductType.SERVICE,
                name="Enchape de baño completo (ejemplo)",
                short_description="Instalación de enchape en piso y paredes, incluye mano de obra.",
                price=1200000,
                price_is_estimate=True,
                unit="proyecto",
                stock=0,
                is_featured=True,
                specs={"Incluye": "Materiales + mano de obra", "Tiempo estimado": "5-7 días"},
            ),
            dict(
                category=categories["remodelaciones"],
                product_type=Product.ProductType.SERVICE,
                name="Pintura de fachada (ejemplo)",
                short_description="Aplicación de pintura exterior, precio según metraje.",
                price=450000,
                price_is_estimate=True,
                unit="proyecto",
                stock=0,
                specs={"Incluye": "Andamios + pintura + mano de obra"},
            ),
        ]
        for data in demo_products:
            Product.objects.get_or_create(name=data.pop("name"), defaults=data)
        self.stdout.write(self.style.SUCCESS("Catálogo de ejemplo creado."))

        demo_projects = [
            dict(
                title="Edificio residencial Los Alcázares (ejemplo)",
                category=Project.Category.RESIDENTIAL,
                location="Medellín",
                year=2023,
                sqm=3200,
                summary="Acabados completos de pisos y enchapes en 48 apartamentos.",
                is_featured=True,
                order=1,
            ),
            dict(
                title="Local comercial Unicentro (ejemplo)",
                category=Project.Category.COMMERCIAL,
                location="Medellín",
                year=2022,
                sqm=850,
                summary="Remodelación integral de fachada y pisos técnicos.",
                is_featured=True,
                order=2,
            ),
            dict(
                title="Bodega industrial Girardota (ejemplo)",
                category=Project.Category.INDUSTRIAL,
                location="Girardota, Antioquia",
                year=2021,
                sqm=6000,
                summary="Piso epóxico industrial y sistema de impermeabilización de cubierta.",
                is_featured=True,
                order=3,
            ),
        ]
        for data in demo_projects:
            Project.objects.get_or_create(title=data.pop("title"), defaults=data)
        self.stdout.write(self.style.SUCCESS("Proyectos de portafolio de ejemplo creados."))

        self.stdout.write(self.style.WARNING("Recuerda: todo lo marcado '(ejemplo)' debe reemplazarse con datos reales."))
