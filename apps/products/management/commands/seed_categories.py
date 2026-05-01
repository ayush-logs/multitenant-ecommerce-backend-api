from django.core.management.base import BaseCommand

from apps.products.models import Category


class Command(BaseCommand):
    help = 'Seed products app with category data'

    def handle(self, *args, **options):
        # Clear existing data
        self.stdout.write('🗑️  Clearing existing categories...')
        Category.objects.all().delete()

        # Create sample categories
        # Main categories (will have products seeded)
        categories_data = [
            {
                "name": "Running Shoes",
            },
            {
                "name": "Basketball Shoes",
            },
            {
                "name": "Casual Shoes",
            },
            {
                "name": "Lifestyle Shoes",
            },
            {
                "name": "Casual Wear",
            },
            {
                "name": "Electronics",
            },
            {
                "name": "Accessories",
            },
            # Edge case categories (no products will be seeded for these)
            {
                "name": "Premium Footwear",
            },
            {
                "name": "Limited Edition",
            },
        ]

        for category_data in categories_data:
            Category.objects.create(**category_data)

        # Summary
        main_categories = 7
        edge_case_categories = 2
        total_categories = len(categories_data)

        self.stdout.write(
            self.style.SUCCESS(f'✓ Created {total_categories} categories')
        )
        self.stdout.write(f'  • {main_categories} main categories (with products)')
        self.stdout.write(f'  • {edge_case_categories} edge case categories (0 products for testing)')
