from django.urls import path

from apps.products.views import (
    CategoryListAPIView,
    CategoryDetailAPIView,
    ProductListAPIView,
    ProductDetailAPIView,
)

urlpatterns = [
    # Category endpoints
    path("categories/", CategoryListAPIView.as_view(), name="category-list"),
    path(
        "categories/<slug:slug>/",
        CategoryDetailAPIView.as_view(),
        name="category-detail",
    ),
    # Product endpoints
    path("products/", ProductListAPIView.as_view(), name="product-list"),
    path(
        "products/<slug:product_slug>/",
        ProductDetailAPIView.as_view(),
        name="product-detail",
    ),
]
