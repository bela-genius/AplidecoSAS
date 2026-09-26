from django.urls import path

from . import views

app_name = "cms"

urlpatterns = [
    path("", views.home, name="home"),
    path("proyectos/", views.project_list, name="projects"),
    path("contacto/", views.contact, name="contact"),
    path("p/<slug:slug>/", views.page_detail, name="page_detail"),
]
