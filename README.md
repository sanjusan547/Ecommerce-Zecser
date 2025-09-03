🛒 E-Commerce Django Project
Project Overview

This is a full-featured e-commerce application built with Django and Django REST Framework.
Features include:

User registration & authentication (JWT optional)

Product catalog with categories and variants

Shopping cart & wishlist

Direct purchase (“Buy Now”) and cart checkout

Razorpay payment integration

Order management

Admin panel for managing products, stock, and orders

Technologies Used

Python 3.13

Django 5.2

Django REST Framework

SQLite 

Razorpay API for payments



Project Setup
1️⃣ Clone the repository
git clone https://github.com/yourusername/ecommerce-Zecser.git


2️⃣ Create a virtual environment
python -m venv env
source env/bin/activate        # Linux / Mac
env\Scripts\activate           # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Database Setup

Default: SQLite (already configured)


5️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Create Superuser
python manage.py createsuperuser  or create with endpoint for admin creation 


Access admin panel at: http://127.0.0.1:8000/admin/

7️⃣ Configure Razorpay

Sign up for Razorpay
.

Get API Key ID and API Key Secret.

Add them to .env or settings.py:

RAZORPAY_KEY_ID = 'your_key_id'
RAZORPAY_KEY_SECRET = 'your_key_secret'


Use sandbox/test mode for development.

8️⃣ Run Development Server
python manage.py runserver


Open in browser: http://127.0.0.1:8000/

Email Configuration

To enable email notifications (e.g., for order confirmations), follow these steps:

Enable 2-Step Verification in your Gmail account

Go to your Google Account → Security → 2-Step Verification → Turn it on.

Generate an App Password

Under Security → App passwords, generate a new password for your app (choose Mail / Other).

Copy the 16-character app password.

Create a .env file in your project root (if not already created):

touch .env        # Linux / Mac
type nul > .env   # Windows


Add email credentials to .env:

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your_email@gmail.com


Update settings.py to read .env:

from decouple import config

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')