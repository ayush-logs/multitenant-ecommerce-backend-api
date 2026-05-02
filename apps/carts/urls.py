from django.urls import path

from apps.carts.views import (
    CartView,
    CartItemAddView,
    CartItemDetailView,
)

urlpatterns = [
    path("cart/", CartView.as_view()),
    path("cart/items/", CartItemAddView.as_view()),
    path("cart/items/<int:pk>/", CartItemDetailView.as_view()),
]
