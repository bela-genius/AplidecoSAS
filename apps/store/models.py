from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    class Icon(models.TextChoices):
        FLOOR = "floor", "Pisos"
        TILE = "tile", "Enchapes"
        PAINT = "paint", "Pintura"
        WALL = "wall", "Muros / drywall"
        ROOF = "roof", "Cubiertas / azoteas"
        WATERPROOF = "waterproof", "Impermeabilización"
        TOOLS = "tools", "Herramientas"
        REMODEL = "remodel", "Remodelación integral"

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    short_pitch = models.CharField(
        max_length=140, blank=True, help_text="Frase corta para la card de servicios en el home."
    )
    icon = models.CharField(max_length=20, choices=Icon.choices, default=Icon.TOOLS)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    show_as_service = models.BooleanField(
        default=True, help_text="Mostrar esta categoría en la sección de servicios del home."
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    class ProductType(models.TextChoices):
        MATERIAL = "material", "Material / producto"
        SERVICE = "service", "Servicio / paquete"

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products"
    )
    product_type = models.CharField(
        max_length=20, choices=ProductType.choices, default=ProductType.MATERIAL
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Para servicios, usar el precio 'desde' o base de la cotización.",
    )
    price_is_estimate = models.BooleanField(
        default=False,
        help_text="Marca esta opción si el precio es una referencia y debe cotizarse (típico en servicios).",
    )
    compare_at_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    stock = models.PositiveIntegerField(
        default=0, help_text="Solo aplica a materiales/productos físicos."
    )
    unit = models.CharField(
        max_length=30,
        blank=True,
        default="unidad",
        help_text="Unidad de venta: m², galón, unidad, caja, etc.",
    )
    sku = models.CharField(max_length=64, unique=True, blank=True, null=True)
    specs = models.JSONField(
        default=dict,
        blank=True,
        help_text="Ficha técnica como pares clave-valor, ej. {'Resistencia': 'PEI 4', 'Formato': '60x60 cm'}",
    )
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    @property
    def is_service(self) -> bool:
        return self.product_type == self.ProductType.SERVICE

    @property
    def is_in_stock(self) -> bool:
        if self.is_service:
            return True
        return self.stock > 0

    @property
    def cta_label(self) -> str:
        return "Solicitar cotización" if self.is_service else "Añadir al carrito"

    @property
    def discount_percent(self) -> int:
        if self.compare_at_price and self.compare_at_price > self.price:
            diff = self.compare_at_price - self.price
            return int((diff / self.compare_at_price) * 100)
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=150, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return f"Imagen de {self.product.name}"


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="cart"
    )
    session_key = models.CharField(max_length=64, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self) -> Decimal:
        return sum((item.subtotal for item in self.items.all()), Decimal("0"))

    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self.items.all())

    def __str__(self) -> str:
        return f"Carrito #{self.pk}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    @property
    def subtotal(self) -> Decimal:
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return f"{self.quantity} x {self.product.name}"


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        PAID = "paid", "Pagado"
        PROCESSING = "processing", "En preparación"
        SHIPPED = "shipped", "Enviado"
        DELIVERED = "delivered", "Entregado"
        CANCELLED = "cancelled", "Cancelado"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders"
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    shipping_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Pedido #{self.pk} - {self.full_name}"

    def recalculate_total(self) -> None:
        self.total = sum((item.subtotal for item in self.items.all()), Decimal("0"))
        self.save(update_fields=["total"])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity

    def __str__(self) -> str:
        return f"{self.quantity} x {self.product_name}"
