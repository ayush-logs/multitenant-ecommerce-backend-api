from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError
from apps.carts.models import Cart
from apps.products.models import Product
from .models import Order, OrderItem


def create_order_from_cart(user) -> Order:
    with transaction.atomic():
        # 1. Fetch user's cart
        try:
            cart = Cart.objects.prefetch_related("items__product").get(user=user)
        except Cart.DoesNotExist:
            raise ValidationError("Cart not found.")

        cart_items = list(
            cart.items.all()
        )  # Evaluate queryset to prevent multiple DB hits
        if not cart_items:
            raise ValidationError("Cart is empty.")

        # 2. Extract product IDs and lock their rows in the database
        product_ids = [item.product_id for item in cart_items]

        # select_for_update() locks these rows until the transaction commits/rolls back
        locked_products = {
            product.id: product
            for product in Product.objects.select_for_update().filter(
                id__in=product_ids
            )
        }

        # 3. Validate stock against the freshly locked database values
        for item in cart_items:
            db_product = locked_products.get(item.product_id)
            if not db_product:
                raise ValidationError(
                    f"Product '{item.product.name}' no longer exists."
                )

            if item.quantity > db_product.stock:
                raise ValidationError(
                    f"{db_product.name}: only {db_product.stock} units available."
                )

        # 4. Calculate total using locked prices (ensuring accurate pricing at checkout)
        total = sum(
            locked_products[item.product_id].price * item.quantity
            for item in cart_items
        )

        # 5. Create the Order
        order = Order.objects.create(user=user, total=total)

        # 6. Bulk create OrderItems and update stock via F() expressions
        order_items = []
        for item in cart_items:
            db_product = locked_products[item.product_id]

            # Prepare OrderItem snapshot
            order_items.append(
                OrderItem(
                    order=order,
                    product=db_product,
                    product_name=db_product.name,
                    unit_price=db_product.price,
                    quantity=item.quantity,
                )
            )

            # Safely decrement stock using an F() expression to avoid race conditions
            db_product.stock = F("stock") - item.quantity
            db_product.save(update_fields=["stock"])

        OrderItem.objects.bulk_create(order_items)

        # 7. Clear the cart
        cart.items.all().delete()

        return order
