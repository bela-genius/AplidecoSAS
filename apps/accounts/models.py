from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Usuario con nivel de acceso especial para paneles internos."""

    class Role(models.TextChoices):
        SUPERADMIN = "superadmin", "Super administrador"
        ADMIN = "admin", "Administrador"
        STAFF = "staff", "Staff / Operaciones"
        EDITOR = "editor", "Editor de contenido"
        CUSTOMER = "customer", "Cliente"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )
    phone = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    @property
    def is_backoffice(self) -> bool:
        return self.role in {
            self.Role.SUPERADMIN,
            self.Role.ADMIN,
            self.Role.STAFF,
            self.Role.EDITOR,
        }

    def __str__(self) -> str:
        return self.get_full_name() or self.username
