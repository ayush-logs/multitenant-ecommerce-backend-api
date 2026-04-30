from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Seed accounts app with dummy data"

    def handle(self, *args, **options):
        # Clear existing data
        self.stdout.write("🗑️  Clearing existing users...")
        User.objects.all().delete()

        # Create sample users
        users_data = [
            # Create merchants
            {
                "username": "merchant1",
                "email": "merchant1@example.com",
                "password": "pass123",
                "role": User.Roles.MERCHANT,
            },
            {
                "username": "merchant2",
                "email": "merchant2@example.com",
                "password": "pass123",
                "role": User.Roles.MERCHANT,
            },
            {
                "username": "merchant3",
                "email": "merchant3@example.com",
                "password": "pass123",
                "role": User.Roles.MERCHANT,
            },
            # Create customers
            {
                "username": "customer1",
                "email": "customer1@example.com",
                "password": "pass123",
                "role": User.Roles.CUSTOMER,
            },
            {
                "username": "customer2",
                "email": "customer2@example.com",
                "password": "pass123",
                "role": User.Roles.CUSTOMER,
            },
        ]

        for user_data in users_data:
            is_merchant = user_data.get("role") == User.Roles.MERCHANT
            user_data["is_merchant"] = is_merchant
            user = User.objects.create_user(**user_data)
            user.save()

        self.stdout.write(self.style.SUCCESS("✓ Accounts seeded successfully"))
