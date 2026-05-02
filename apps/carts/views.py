from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.carts.models import Cart, CartItem
from apps.carts.serializers import (
    CartItemAddSerializer,
    CartSerializer,
    CartItemUpdateSerializer,
)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemAddView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemAddSerializer

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemUpdateSerializer
    http_method_names = ["patch", "delete"]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
