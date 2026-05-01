from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.accounts.permissions import IsMerchant
from apps.products.models import Product, Category
from apps.products.serializers import (
    CategoryListSerializer,
    CategoryDetailSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductMerchantCreateSerializer,
)
from apps.stores.models import Store


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [AllowAny]


class CategoryDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CategoryDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Category.objects.prefetch_related("products")


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Product.objects.select_related("category").all()


class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Product.objects.select_related("category").all()


class ProductMerchantAPIView(generics.ListCreateAPIView):
    permission_classes = [IsMerchant, IsAuthenticated]

    def get_queryset(self):
        store_id = self.kwargs["store_id"]
        return Product.objects.filter(
            store__id=store_id, store__owner=self.request.user
        )

    def perform_create(self, serializer):
        store = get_object_or_404(
            Store, id=self.kwargs["store_id"], owner=self.request.user
        )
        serializer.save(store=store)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductMerchantCreateSerializer
        return ProductListSerializer


class ProductMerchantDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsMerchant, IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        store_id = self.kwargs["store_id"]
        return Product.objects.filter(
            store__id=store_id, store__owner=self.request.user
        )

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return ProductMerchantCreateSerializer
        return ProductDetailSerializer
