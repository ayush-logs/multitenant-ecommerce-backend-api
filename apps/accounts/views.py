from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer, User
from rest_framework import generics


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
