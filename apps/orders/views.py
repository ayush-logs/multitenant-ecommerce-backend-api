# apps/orders/views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError

from .models import Order
from .serializers import OrderListSerializer, OrderDetailSerializer
from .services import create_order_from_cart  # Import your service


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
            # Delegate all business logic to the service
            order = create_order_from_cart(user=request.user)

            serializer = OrderDetailSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            # Catch business logic errors and return them as 400 Bad Request
            return Response(
                {"detail": e.message if hasattr(e, "message") else list(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items")
