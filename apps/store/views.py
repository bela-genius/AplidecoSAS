from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import get_or_create_cart
from .models import Category, Order, OrderItem, Product


def product_list(request):
    products = Product.objects.filter(is_active=True)
    category_slug = request.GET.get("categoria")
    if category_slug:
        products = products.filter(category__slug=category_slug)
    query = request.GET.get("q")
    if query:
        products = products.filter(name__icontains=query)

    context = {
        "products": products,
        "categories": Category.objects.filter(is_active=True),
        "selected_category": category_slug,
        "query": query or "",
    }
    return render(request, "store/product_list.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "store/product_detail.html", {"product": product})


def cart_detail(request):
    cart = get_or_create_cart(request)
    return render(request, "store/cart_detail.html", {"cart": cart})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get("quantity", 1))

    item, created = cart.items.get_or_create(product=product, defaults={"quantity": quantity})
    if not created:
        item.quantity += quantity
        item.save()

    messages.success(request, f"{product.name} se añadió al carrito.")
    return redirect("store:cart_detail")


@require_POST
def cart_remove(request, item_id):
    cart = get_or_create_cart(request)
    cart.items.filter(id=item_id).delete()
    return redirect("store:cart_detail")


def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.warning(request, "Tu carrito está vacío.")
        return redirect("store:product_list")

    if request.method == "POST":
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=request.POST.get("full_name", ""),
            email=request.POST.get("email", ""),
            phone=request.POST.get("phone", ""),
            shipping_address=request.POST.get("shipping_address", ""),
            city=request.POST.get("city", ""),
            notes=request.POST.get("notes", ""),
        )
        for item in cart.items.select_related("product"):
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                unit_price=item.product.price,
                quantity=item.quantity,
            )
        order.recalculate_total()
        cart.items.all().delete()
        return render(request, "store/order_success.html", {"order": order})

    return render(request, "store/checkout.html", {"cart": cart})
