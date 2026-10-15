from django.urls import path

from . import views

app_name = "cms"

urlpatterns = [
    path("", views.home, name="home"),
    path("quienes-somos/", views.about, name="about"),
    path("catalogo/", views.catalog, name="catalog"),
    path("chatbot/", views.chatbot, name="chatbot"),
    path("proyectos/", views.project_list, name="projects"),
    path("agenda/", views.schedule, name="schedule"),
    path("contacto/", views.contact, name="contact"),
    path("p/<slug:slug>/", views.page_detail, name="page_detail"),
]
