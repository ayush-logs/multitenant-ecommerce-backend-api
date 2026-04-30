# Multitenant E-commerce Backend API

A Django-based REST API for a multitenant e-commerce platform with support for multiple stores, products, and categories.

## Features

- **Multi-tenancy**: Support for multiple stores/vendors on a single codebase
- **Custom User Model**: Email-based authentication with role-based access (Customer/Merchant)
- **JWT Authentication**: Secure token-based authentication with refresh tokens
- **Product Management**: Complete CRUD operations for products with categories
- **Store Management**: Merchants can create and manage their stores
- **Category System**: Hierarchical product categorization
- **REST API**: Built with Django REST Framework
- **API Documentation**: Interactive Swagger UI and ReDoc documentation
- **Environment Configuration**: Using django-environ for settings management
- **Database Seeding**: Automated data seeding for development and testing

## Tech Stack

- **Framework**: Django 5.2
- **API**: Django REST Framework
- **Authentication**: Django REST Framework Simple JWT
- **Documentation**: drf-spectacular (Swagger/ReDoc)
- **Database**: SQLite (default) / PostgreSQL
- **Environment**: django-environ

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd multitenant-ecommerce-backend-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Seed the database** (optional)
   ```bash
   python manage.py seed
   ```

7. **Create superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
multitenant-ecommerce-backend-api/
├── apps/
│   ├── accounts/              # User authentication & profiles
│   │   ├── models.py          # Custom User model with roles
│   │   ├── serializers.py     # Registration & user serializers
│   │   ├── views.py           # Authentication views
│   │   ├── permissions.py     # Role-based permissions
│   │   └── tests.py           # Unit tests
│   ├── products/              # Product & category management
│   │   ├── models.py          # Product & Category models
│   │   ├── serializers.py     # Product & category serializers
│   │   ├── views.py           # Product & category views
│   │   └── management/        # Database seeding
│   └── stores/                # Store management for merchants
│       ├── models.py          # Store model
│       ├── serializers.py     # Store serializers
│       ├── views.py           # Store CRUD views
│       └── management/        # Database seeding
├── config/
│   ├── settings.py            # Django settings
│   ├── urls.py                # URL routing
│   ├── asgi.py                # ASGI config
│   ├── wsgi.py                # WSGI config
│   └── management/commands/   # Global management commands
├── .env                       # Environment variables
├── .env.example               # Environment template
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── db.sqlite3                 # SQLite database
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `SECRET_KEY` | Django secret key | (required) |
| `ALLOWED_HOSTS` | Allowed host domains | `[]` |
| `DATABASE_ENGINE` | Database engine | `django.db.backends.sqlite3` |
| `DATABASE_NAME` | Database name | `db.sqlite3` |

## Database Seeding

The project includes automated seeding for development and testing:

### Seed All Data
```bash
python manage.py seed
```

### Seed Specific Apps
```bash
python manage.py seed_accounts      # Seed users (admin, customers, merchants)
python manage.py seed_stores        # Seed sample stores
python manage.py seed_categories    # Seed product categories
python manage.py seed_products      # Seed sample products
```

### Seed Individual App
```bash
python manage.py seed --app accounts
python manage.py seed --app stores
python manage.py seed --app categories
python manage.py seed --app products
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/login/` - User login (JWT tokens)
- `POST /api/v1/auth/token/refresh/` - Refresh access token

### Categories
- `GET /api/v1/categories/` - List all categories
- `GET /api/v1/categories/{slug}/` - Get category details with products

### Products
- `GET /api/v1/products/` - List all products (with category info)
- `GET /api/v1/products/{slug}/` - Get product details

### Stores (Merchant Only)
- `POST /api/v1/stores/` - Create a new store
- `GET /api/v1/stores/` - List merchant's stores
- `GET /api/v1/stores/{id}/` - Get store details
- `PUT /api/v1/stores/{id}/` - Update store
- `PATCH /api/v1/stores/{id}/` - Partial update store

### API Documentation
- `GET /api/schema/swagger-ui/` - Interactive Swagger UI
- `GET /api/schema/redoc/` - ReDoc documentation
- `GET /api/schema/` - OpenAPI schema

## User Roles

- **Customer**: Can browse products and categories
- **Merchant**: Can create/manage stores, products (future feature)

## Testing

Run the test suite:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License