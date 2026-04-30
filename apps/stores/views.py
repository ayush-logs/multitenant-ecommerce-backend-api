from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.stores.serializers import StoreSerializer, StoreCreateSerializer
from .models import Store
from ..accounts.permissions import IsMerchant


class StoreCreateAPIView(generics.CreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreCreateSerializer
    permission_classes = [IsAuthenticated, IsMerchant]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class StoreListPIView(generics.ListAPIView):
    serializer_class = StoreCreateSerializer
    permission_classes = [IsAuthenticated, IsMerchant]

    def get_queryset(self):
        return Store.objects.filter(owner=self.request.user)


class StoreDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated, IsMerchant]

    def get_object(self):
        return get_object_or_404(Store, pk=self.kwargs["pk"])
