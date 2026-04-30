from django.core.management.base import BaseCommand

from apps.products.models import Product, Category


class Command(BaseCommand):
    help = 'Seed products app with dummy data'

    def handle(self, *args, **options):
        # Clear existing data
        self.stdout.write('🗑️  Clearing existing products...')
        Product.objects.all().delete()

        # Create sample products
        products_data = [
            {
                "name": "Air Max 90",
                "description": "Classic running shoe with cushioned sole",
                "price": 129.99,
                "stock": 50,
                "category": Category.objects.get(slug="running-shoes")
            },
            {
                "name": "Ultraboost 22",
                "description": "Premium performance running shoe with responsive cushioning",
                "price": 189.99,
                "stock": 30,
                "category": Category.objects.get(slug="running-shoes")
            },
            {
                "name": "Jordan 1 Retro",
                "description": "Iconic basketball shoe with premium leather construction",
                "price": 169.99,
                "stock": 25,
                "category": Category.objects.get(slug="basketball-shoes")
            },
            {
                "name": "Blazer Mid",
                "description": "Vintage-inspired court shoe perfect for casual wear",
                "price": 89.99,
                "stock": 40,
                "category": Category.objects.get(slug="casual-shoes")
            },
            {
                "name": "New Balance 990v6",
                "description": "American-made lifestyle shoe with premium comfort",
                "price": 174.99,
                "stock": 20,
                "category": Category.objects.get(slug="lifestyle-shoes")
            },
        ]

        for product_data in products_data:
            Product.objects.create(**product_data)

        self.stdout.write(self.style.SUCCESS('✓ Products seeded successfully'))
