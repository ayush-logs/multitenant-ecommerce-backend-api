# Multitenant E-commerce Backend API

A Django-based REST API for a multitenant e-commerce platform with support for multiple stores.

## Features

- **Multi-tenancy**: Support for multiple stores/vendors on a single codebase
- **Custom User Model**: Email-based authentication
- **REST API**: Built with Django REST Framework
- **Environment Configuration**: Using django-environ for settings management

## Tech Stack

- **Framework**: Django 5.2
- **API**: Django REST Framework
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

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
multitenant-ecommerce-backend-api/
├── apps/
│   └── accounts/          # User authentication app
├── config/
│   ├── settings.py         # Django settings
│   ├── urls.py             # URL routing
│   ├── asgi.py             # ASGI config
│   └── wsgi.py             # WSGI config
├── .env                    # Environment variables
├── .env.example            # Environment template
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `True` |
| `SECRET_KEY` | Django secret key | (required) |
| `ALLOWED_HOSTS` | Allowed host domains | `localhost,127.0.0.1` |
| `DATABASE_ENGINE` | Database engine | `django.db.backends.sqlite3` |
| `DATABASE_NAME` | Database name | `db.sqlite3` |

## API Endpoints

> To be added as endpoints are implemented

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License