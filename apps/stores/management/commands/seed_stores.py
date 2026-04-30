from django.core.management.base import BaseCommand
from apps.stores.models import Store
from apps.accounts.models import User


class Command(BaseCommand):
    help = 'Seed stores app with dummy data'

    def handle(self, *args, **options):
        # Clear existing stores
        Store.objects.all().delete()
        self.stdout.write(self.style.WARNING('🗑️  Cleared existing stores'))

        # Get merchants (users with is_merchant=True)
        merchants = User.objects.filter(is_merchant=True)
        if not merchants.exists():
            self.stdout.write(
                self.style.ERROR('❌ No merchants found. Run seed_accounts first.')
            )
            return

        # Create sample stores
        stores_data = [
            {
                "name": "Nike Official Store",
                "description": "Official Nike store with premium athletic footwear and apparel",
                "phone": "+1-555-0123",
                "address": "123 Sports Avenue, New York, NY 10001",
                "owner": merchants[0] if merchants else None,
            },
            {
                "name": "Adidas Performance",
                "description": "Premium Adidas products for athletes and fitness enthusiasts",
                "phone": "+1-555-0124",
                "address": "456 Fitness Blvd, Los Angeles, CA 90210",
                "owner": merchants[0] if merchants else None,
            },
            {
                "name": "Puma Athletic Center",
                "description": "Puma's finest collection of running and training gear",
                "phone": "+1-555-0125",
                "address": "789 Runner's Way, Chicago, IL 60601",
                "owner": merchants[0] if merchants else None,
            },
        ]

        for store_data in stores_data:
            Store.objects.create(**store_data)

        self.stdout.write(
            self.style.SUCCESS(f'✓ Created {len(stores_data)} stores successfully')
        )
