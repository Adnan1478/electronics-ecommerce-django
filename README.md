# Electronics E-commerce Website using Django

Electronics E-commerce Website is a web-based application developed using Django. This project allows users to browse electronic products, view product details, add products to cart, and place orders. It also provides an admin panel to manage products, categories, users, and orders.

This project is created for learning and academic purposes and demonstrates important Django concepts such as models, views, templates, authentication, database management, cart functionality, order management, and admin panel customization.

## Features

### User Features

- User registration and login
- Browse electronic products
- View product details
- Search products
- Filter products by category
- Add products to cart
- Update cart quantity
- Remove products from cart
- Checkout and place orders
- View order details
- Responsive design for mobile and desktop

### Admin Features

- Admin login
- Add new products
- Update product details
- Delete products
- Manage product categories
- Manage users
- Manage customer orders
- View order information using Django admin panel

## Tech Stack

### Frontend

- HTML5
- CSS3
- Bootstrap
- JavaScript

### Backend

- Python
- Django
- Django ORM

### Database

- SQLite / MySQL

## Project Structure

```txt
electronics-ecommerce-django/
│
├── ecommerce/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── store/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
│
├── templates/
│   └── store/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
Environment Variables

Create a .env file in the project root folder and add your secret values:

SECRET_KEY=your_django_secret_key_here
DEBUG=True

Do not upload the .env file to GitHub.

Installation and Setup
1. Clone the Repository
git clone https://github.com/Adnan1478/electronics-ecommerce-django.git
cd electronics-ecommerce-django
2. Create Virtual Environment
python -m venv venv
3. Activate Virtual Environment

For Windows:

venv\Scripts\activate

For macOS/Linux:

source venv/bin/activate
4. Install Requirements
pip install -r requirements.txt
5. Run Migrations
python manage.py makemigrations
python manage.py migrate
6. Create Superuser
python manage.py createsuperuser
7. Run Development Server
python manage.py runserver

Open the project in browser:

http://127.0.0.1:8000/
Main Modules
User Authentication Module
Product Management Module
Category Management Module
Cart Management Module
Checkout Module
Order Management Module
Admin Panel Module
Screenshots

Below are some screenshots of the Electronics E-commerce Website showing user and admin features.
```

### Home Page
<img width="100%" alt="Home Page" src="https://github.com/user-attachments/assets/1edc7e7f-2a84-41d8-bef1-0de918c598f4" />

Product Listing Page
<img width="100%" alt="Product Listing Page" src="https://github.com/user-attachments/assets/822e134b-08a7-4317-9380-561888c2cbd3" />

### Cart Page
<img width="100%" alt="Cart Page" src="https://github.com/user-attachments/assets/d9d4a782-73c9-4989-a6bb-abda600a29f0" />

### Checkout Page
<img width="100%" alt="Checkout Page" src="https://github.com/user-attachments/assets/356687a4-e0a0-482f-a4f7-c285b053b58c" />

### Admin Dashboard
<img width="100%" alt="Admin Product Management" src="https://github.com/user-attachments/assets/52284d41-af1f-4362-a00d-c81336cb670d" />

### Admin Product Listing
<img width="100%" alt="Admin Product Listing" src="https://github.com/user-attachments/assets/7fb3b548-b448-4e5d-ae66-68a0cd417277" />


### Admin Order Listing
<img width="100%" alt="Admin Order Listing" src="https://github.com/user-attachments/assets/3eeaf3fa-18ae-43e1-849c-66c4ad5af9df" />


Author

Adnan Mansuri

GitHub: Adnan1478
