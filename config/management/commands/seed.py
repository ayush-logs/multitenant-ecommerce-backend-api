from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Run all seed commands for the project'

    def add_arguments(self, parser):
        parser.add_argument(
            '--app',
            type=str,
            help='Seed a specific app (e.g., accounts, products)',
        )

    def handle(self, *args, **options):
        app = options.get('app')

        if app:
            # Seed specific app
            try:
                call_command(f'seed_{app}')
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Seeded {app} app successfully')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error seeding {app} app: {str(e)}')
                )
        else:
            # Seed all apps
            self.stdout.write(self.style.SUCCESS('🌱 Starting seed process...'))
            commands = ['seed_accounts', 'seed_stores', 'seed_categories', 'seed_products']

            for command in commands:
                try:
                    call_command(command)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Error running {command}: {str(e)}')
                    )

            self.stdout.write(
                self.style.SUCCESS('✓ All seeds completed successfully!')
            )
