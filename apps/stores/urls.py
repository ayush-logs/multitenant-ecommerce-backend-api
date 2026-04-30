from django.urls import path

from apps.stores.views import StoreCreateAPIView, StoreListPIView, StoreDetailAPIView

urlpatterns = [
    path("", StoreCreateAPIView.as_view()),
    path("mine/", StoreListPIView.as_view()),
    path("mine/<int:pk>/", StoreDetailAPIView.as_view()),
]
