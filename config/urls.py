from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.cms.urls")),
    path("tienda/", include("apps.store.urls")),
    path("cuenta/", include("apps.accounts.urls")),
    path("api/chatbot/", include("apps.chatbot.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
