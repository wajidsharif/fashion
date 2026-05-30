# F for Fashion - Premium Online Clothing Store

A modern, fully-functional Django-based online clothing store with WhatsApp ordering, responsive design, and Tailwind CSS.

## Tech Stack

- **Backend:** Django 6.0
- **Database:** SQLite
- **Frontend:** Tailwind CSS 3 + Alpine.js
- **Payment:** WhatsApp Order Integration
- **Admin:** Django Admin Panel

## Features

- Mobile-first responsive design
- Product catalog with categories, sizes, colors
- Advanced shop page with filtering & search
- AJAX shopping cart
- WhatsApp order integration
- SEO optimized with sitemap & robots.txt
- Modern fashion UI

## Quick Start

### 1. Setup Virtual Environment

```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Tailwind CSS

```bash
npm install
npm run build:css
```

For development (auto-rebuild):
```bash
npm run watch:css
```

### 4. Configure Environment

Copy settings from `.env` file (already configured for development).

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Seed Sample Data

```bash
python manage.py seed_data
```

### 8. Run Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/

## Admin Panel

http://127.0.0.1:8000/admin/

Default admin credentials (if created via seed): `admin` / `admin123`

## WhatsApp Integration

WhatsApp number is configured in `.env`:
```
WHATSAPP_NUMBER=+923104869233
```

## Project Structure

```
FFF_V2/
├── fashion/              # Project settings
├── core/                 # Core app (homepage, context processors)
├── products/             # Products app (models, shop, detail)
├── cart/                 # Cart app (AJAX session cart)
├── orders/               # Orders app (checkout, WhatsApp)
├── templates/            # Django templates
│   ├── core/             # Homepage
│   ├── products/         # Shop & product detail
│   ├── cart/             # Cart page
│   ├── orders/           # Checkout & success
│   └── partials/         # Navbar, footer, messages
├── static/               # Static assets
│   ├── css/              # Tailwind CSS
│   └── js/               # JavaScript
├── media/                # User uploads
├── venv/                 # Virtual environment
├── node_modules/         # Node dependencies
├── requirements.txt      # Python dependencies
├── package.json          # Node dependencies
├── tailwind.config.js    # Tailwind configuration
└── .env                  # Environment variables
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `python manage.py runserver` | Start development server |
| `npm run build:css` | Build Tailwind CSS (production) |
| `npm run watch:css` | Watch & rebuild Tailwind CSS |
| `python manage.py seed_data` | Seed sample data |
| `python manage.py migrate` | Run migrations |
| `python manage.py makemigrations` | Create migrations |

## License

MIT
