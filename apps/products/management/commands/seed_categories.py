from django.core.management.base import BaseCommand

from apps.products.models import Category


class Command(BaseCommand):
    help = 'Seed products app with category data'

    def handle(self, *args, **options):
        # Clear existing data
        self.stdout.write('🗑️  Clearing existing categories...')
        Category.objects.all().delete()

        # Create sample categories
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
        ]

        for category_data in categories_data:
            Category.objects.create(**category_data)

        self.stdout.write(self.style.SUCCESS('✓ Categories seeded successfully'))
