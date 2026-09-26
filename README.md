# AplidecoSAS

Plataforma web para Aplideco S.A.S.: e-commerce, sitio informativo/branding con enlaces a redes sociales,
panel con accesos por rol y un asistente (chatbot) de información puntual.

## Stack

- Django 5.2 + Django REST Framework
- SQLite en desarrollo (configurable vía `DATABASE_URL`)
- Tailwind CSS (CDN) + AOS para animaciones en el frontend
- Chatbot basado en reglas (palabras clave), gestionable desde el admin

## Estructura

```
config/          # Settings, urls raíz, wsgi/asgi
apps/
  accounts/      # Usuario personalizado con roles (superadmin, admin, staff, editor, customer)
  store/         # Catálogo, carrito, pedidos (e-commerce)
  cms/           # Configuración de marca, páginas informativas, redes sociales
  chatbot/       # Base de conocimiento + endpoint de chat
templates/       # Plantillas HTML (Tailwind + AOS)
static/          # JS/CSS propios (widget de chat, etc.)
```

## Puesta en marcha

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Roles de usuario (`apps.accounts.User.Role`)

- `superadmin` / `admin`: acceso total al panel de Django admin.
- `staff`: operaciones (pedidos, inventario).
- `editor`: contenido (páginas, marca, chatbot).
- `customer`: usuario final de la tienda.

## Próximos pasos sugeridos

- Definir identidad de marca (colores, logo, tono de voz) para cargar en `SiteSettings`.
- Cargar catálogo real de productos y categorías.
- Conectar una pasarela de pago (ej. Wompi/PayU/Stripe) al flujo de checkout.
- Enriquecer el chatbot (más entradas de conocimiento o integrarlo con un modelo de lenguaje).
- Pulir animaciones y diseño visual definitivo de cada sección.
