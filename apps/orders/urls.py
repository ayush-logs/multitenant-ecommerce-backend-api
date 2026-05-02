from django.urls import path
from .views import OrderListCreateView, OrderDetailView

urlpatterns = [
    path("orders/", OrderListCreateView.as_view()),
    path("orders/<int:pk>/", OrderDetailView.as_view()),
]
