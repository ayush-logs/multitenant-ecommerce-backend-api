from django.core.management.base import BaseCommand
import random
from apps.products.models import Product, Category
from apps.stores.models import Store


class Command(BaseCommand):
    help = 'Seed products app with dummy data'

    def handle(self, *args, **options):
        # Clear existing data
        self.stdout.write('🗑️  Clearing existing products...')
        Product.objects.all().delete()

        # Get available stores and categories
        stores = list(Store.objects.all())
        all_categories = list(Category.objects.all())

        if not stores:
            self.stdout.write(
                self.style.ERROR('❌ No stores found. Run seed_stores first.')
            )
            return

        if not all_categories:
            self.stdout.write(
                self.style.ERROR('❌ No categories found. Run seed_categories first.')
            )
            return

        # Define product name templates by category slug
        product_templates = {
            'running-shoes': [
                'Nike Air Zoom Pegasus', 'Adidas Ultraboost', 'Puma Deviate Nitro',
                'Nike React Element', 'Adidas Supernova', 'Puma ForeverRun',
                'Nike ZoomX Vaporfly', 'Adidas Adizero', 'Puma Speed 300'
            ],
            'basketball-shoes': [
                'Nike LeBron Witness', 'Jordan Retro High', 'Adidas Harden Stepback',
                'Nike Kyrie Flytrap', 'Jordan Jumpman', 'Adidas D Rose',
                'Nike Kobe Bryant', 'Jordan Air Ship', 'Adidas Trae Young'
            ],
            'casual-shoes': [
                'Nike Blazer Mid', 'Adidas Stan Smith', 'Puma Suede Classic',
                'Nike Chuck Taylor', 'Adidas Superstar', 'Puma Basket Classic',
                'Nike Cortez', 'Adidas Gazelle', 'Puma Roma'
            ],
            'lifestyle-shoes': [
                'Nike Air Force 1', 'Adidas Yeezy Boost', 'Puma RS-X',
                'Nike Dunk Low', 'Adidas NMD', 'Puma Cali',
                'Nike Air Max 90', 'Adidas Ultraboost', 'Puma Future Rider'
            ],
            'casual-wear': [
                'Cotton T-Shirt', 'Denim Jeans', 'Hooded Sweatshirt',
                'Chinos Pants', 'Polo Shirt', 'Cardigan Sweater',
                'Cargo Shorts', 'V-Neck Sweater', 'Linen Shirt'
            ],
            'electronics': [
                'Wireless Headphones', 'Smart Watch', 'Bluetooth Speaker',
                'Gaming Mouse', 'USB-C Hub', 'Portable Charger',
                'Wireless Earbuds', 'Smartphone Stand', 'LED Desk Lamp'
            ],
            'accessories': [
                'Leather Wallet', 'Sunglasses', 'Backpack', 'Watch',
                'Phone Case', 'Keychain', 'Belt', 'Cap', 'Scarf'
            ]
        }

        # Filter categories to only main categories (with product templates)
        # This ensures edge case categories (Premium Footwear, Limited Edition) remain empty
        categories = [cat for cat in all_categories if cat.slug in product_templates.keys()]
        edge_case_categories = [cat for cat in all_categories if cat not in categories]

        # Generate 50-80 products total
        total_products = random.randint(50, 80)

        # Distribute products across stores unevenly
        # Target: Store 1 → ~5, Store 2 → ~10, Store 3 → ~15, and at least one store with 0
        num_stores = len(stores)
        if num_stores >= 3:
            # Assign to first 2 stores, leave last one with 0
            store_counts = [5, 10, 15][:num_stores-1] + [0]  # Ensure last has 0
            random.shuffle(store_counts[:-1])  # Shuffle the non-zero counts
            store_counts = store_counts[:num_stores]  # Trim to actual stores
        else:
            # For fewer stores, distribute proportionally
            base_counts = [5, 10, 15][:num_stores]
            store_counts = base_counts

        # Adjust total to match our target
        current_total = sum(store_counts)
        if current_total < total_products:
            # Add remaining to random stores (not the one with 0)
            remaining = total_products - current_total
            eligible_stores = [i for i, count in enumerate(store_counts) if count > 0]
            for _ in range(remaining):
                if eligible_stores:
                    idx = random.choice(eligible_stores)
                    store_counts[idx] += 1

        # Generate products
        products_data = []
        store_index = 0
        product_counters = {}  # Track counts for unique naming

        for store_idx, count in enumerate(store_counts):
            if count == 0:
                continue
            for _ in range(count):
                # Select random category
                category = random.choice(categories)
                category_slug = category.slug

                # Get product names for this category
                names = product_templates.get(category_slug, ['Generic Product'])
                base_name = random.choice(names)

                # Ensure unique name by adding counter if needed
                counter = product_counters.get(base_name, 0)
                if counter > 0:
                    name = f"{base_name} {counter}"
                else:
                    name = base_name
                product_counters[base_name] = counter + 1

                # Generate price (999-15000 INR)
                price = round(random.uniform(999, 15000), 2)

                # Generate stock with varied distribution
                stock_options = [0] * 10 + list(range(1, 6)) * 20 + list(range(20, 101)) * 70
                stock = random.choice(stock_options)

                products_data.append({
                    'name': name,
                    'description': f'High-quality {name.lower()} from {stores[store_idx].name}',
                    'price': price,
                    'stock': stock,
                    'category': category,
                    'store': stores[store_idx]
                })

        # Create products
        created_products = []
        for product_data in products_data:
            product = Product.objects.create(**product_data)
            created_products.append(product)

        # Summary
        store_product_counts = {}
        for product in created_products:
            store_name = product.store.name
            store_product_counts[store_name] = store_product_counts.get(store_name, 0) + 1

        self.stdout.write(
            self.style.SUCCESS(f'✓ Created {len(created_products)} products across {len([c for c in store_counts if c > 0])} stores')
        )

        # Show distribution
        for store_name, count in store_product_counts.items():
            self.stdout.write(f'  • {store_name}: {count} product(s)')

        # Show stores with 0 products
        stores_with_zero = [store.name for store in stores if store.name not in store_product_counts]
        if stores_with_zero:
            self.stdout.write(f'  • Stores with 0 products: {", ".join(stores_with_zero)}')

        # Show categories with 0 products (edge case categories)
        if edge_case_categories:
            edge_case_names = [cat.name for cat in edge_case_categories]
            self.stdout.write(
                self.style.WARNING(f'⚠️  Edge case categories (0 products): {", ".join(edge_case_names)}')
            )
