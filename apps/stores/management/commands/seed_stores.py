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
        merchants = list(User.objects.filter(is_merchant=True))
        if not merchants:
            self.stdout.write(
                self.style.ERROR('❌ No merchants found. Run seed_accounts first.')
            )
            return

        # Multi-tenant distribution: Merchant 1 → 1 store, Merchant 2 → 2 stores, Merchant 3 → 0 stores
        stores_data = []

        # Merchant 1 → 1 store
        if len(merchants) >= 1:
            stores_data.append({
                "name": "Nike Mumbai",
                "description": "Official Nike store in Mumbai with premium athletic footwear and apparel",
                "phone": "+91-22-1234-5678",
                "address": "123 Bandra West, Mumbai, Maharashtra 400050",
                "owner": merchants[0],
            })

        # Merchant 2 → 2 stores
        if len(merchants) >= 2:
            stores_data.extend([
                {
                    "name": "Urban Threads Delhi",
                    "description": "Trendy fashion and lifestyle store in the heart of Delhi",
                    "phone": "+91-11-2345-6789",
                    "address": "456 Connaught Place, New Delhi, Delhi 110001",
                    "owner": merchants[1],
                },
                {
                    "name": "TechBazaar India",
                    "description": "Premium electronics and gadgets store with latest technology",
                    "phone": "+91-80-3456-7890",
                    "address": "789 MG Road, Bangalore, Karnataka 560001",
                    "owner": merchants[1],
                }
            ])

        # Merchant 3 → 0 stores (intentionally skipped for edge case testing)

        # Create stores
        created_stores = []
        for store_data in stores_data:
            store = Store.objects.create(**store_data)
            created_stores.append(store)

        # Summary
        merchant_store_counts = {}
        for store in created_stores:
            merchant_email = store.owner.email
            merchant_store_counts[merchant_email] = merchant_store_counts.get(merchant_email, 0) + 1

        self.stdout.write(
            self.style.SUCCESS(f'✓ Created {len(created_stores)} stores across {len(merchant_store_counts)} merchants')
        )

        # Show distribution
        for merchant_email, count in merchant_store_counts.items():
            self.stdout.write(f'  • {merchant_email}: {count} store(s)')
