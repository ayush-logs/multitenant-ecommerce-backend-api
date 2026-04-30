from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model with email as the primary authentication field.
    """

    class Roles(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        MERCHANT = "merchant", "Merchant"

    email = models.EmailField(unique=True)
    role = models.CharField(
        choices=Roles.choices, default=Roles.CUSTOMER, max_length=20
    )
    is_merchant = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email
