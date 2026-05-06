# apps/orders/services.py
from django.db import transaction
from django.core.exceptions import ValidationError
from apps.carts.models import Cart
from .models import Order, OrderItem


def create_order_from_cart(user) -> Order:
    """
    Business logic to convert a User's Cart into an Order.
    Using @transaction.atomic ensures that if any part fails,
    no database changes are saved.
    """
    with transaction.atomic():
        try:
            cart = Cart.objects.prefetch_related("items__product").get(user=user)
        except Cart.DoesNotExist:
            raise ValidationError("Cart not found.")

        cart_items = cart.items.all()
        if not cart_items.exists():
            raise ValidationError("Cart is empty.")

        # 1. Validate Stock
        for item in cart_items:
            if item.quantity > item.product.stock:
                raise ValidationError(
                    f"{item.product.name}: only {item.product.stock} units available."
                )

        # 2. Calculate Total
        total = sum(item.product.price * item.quantity for item in cart_items)

        # 3. Create Order
        order = Order.objects.create(user=user, total=total)

        # 4. Snapshot Items & Deduct Stock
        order_items = []
        for item in cart_items:
            # Prepare OrderItem
            order_items.append(
                OrderItem(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    unit_price=item.product.price,
                    quantity=item.quantity,
                )
            )
            # Deduct stock
            item.product.stock -= item.quantity
            item.product.save()

        OrderItem.objects.bulk_create(order_items)

        # 5. Clear Cart
        cart_items.delete()

        return order
