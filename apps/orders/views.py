from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.carts.models import Cart
from .models import Order, OrderItem
from .serializers import OrderListSerializer, OrderDetailSerializer


class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = (
            Order.objects.filter(user=request.user)
            .prefetch_related("items")
            .order_by("-created_at")
        )
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            cart = Cart.objects.prefetch_related("items__product").get(
                user=request.user
            )
        except Cart.DoesNotExist:
            return Response(
                {"detail": "Cart not found."}, status=status.HTTP_400_BAD_REQUEST
            )

        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response(
                {"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST
            )

        # validate stock before touching anything
        errors = []
        for item in cart_items:
            if item.quantity > item.product.stock:
                errors.append(
                    f"{item.product.name}: only {item.product.stock} units available."
                )
        if errors:
            return Response({"detail": errors}, status=status.HTTP_400_BAD_REQUEST)

        # calculate total
        total = sum(item.product.price * item.quantity for item in cart_items)

        # create order
        order = Order.objects.create(user=request.user, total=total)

        # snapshot each item — price/name preserved even if product changes later
        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                product_name=item.product.name,
                unit_price=item.product.price,
                quantity=item.quantity,
            )
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)

        # deduct stock
        for item in cart_items:
            item.product.stock -= item.quantity
            item.product.save()

        # clear cart
        cart_items.delete()

        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items")
