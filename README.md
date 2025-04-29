# 🛒 MarketplacePy

**Final Project — SoftUni Django Advanced Course**

MarketplacePy is a web application where users can buy and sell items, connect with each other, and leave reviews.  
Built with Django 5.1 and Django REST Framework, it offers a fully functional online marketplace, complete with user authentication, item listings, profile management, and cloud-based media handling

## 🚀 Features

- User registration, login, and profile management
- Create, browse, edit, and delete item listings
- User-to-user messaging (optional)
- Leave reviews and ratings for users
- RESTful API endpoints using Django REST Framework
- Secure authentication and authorization
- Upload and manage images with Cloudinary
- Admin panel for managing users, listings, and reviews
- Responsive front-end templates (if included)

## 🛠️ Technologies Used

- [Django 5.1](https://docs.djangoproject.com/en/5.1/) — High-level Python web framework
- [Django REST Framework (DRF)](https://www.django-rest-framework.org/) — Powerful toolkit for building Web APIs
- [PostgreSQL](https://www.postgresql.org/) — Relational database management system
- [Cloudinary](https://cloudinary.com/) — Cloud-based image storage and management
- [django-cloudinary-storage](https://pypi.org/project/django-cloudinary-storage/) — Integration of Cloudinary with Django
- [Pillow](https://python-pillow.org/) — Image processing for handling uploaded images
- [psycopg2](https://pypi.org/project/psycopg2/) — PostgreSQL adapter for Django
- [Requests](https://requests.readthedocs.io/en/latest/) — HTTP requests handling
- [asgiref](https://pypi.org/project/asgiref/) — ASGI compatibility for Django applications

### 1. Clone the repository

To get started, clone the **MarketplacePy** repository to your local machine:

```bash
git clone https://github.com/Ivaylo1992/MarketplacePy.git
cd MarketplacePy
```

### 2. Create and activate a virtual environment

It is recommended to create a virtual environment to manage dependencies for this project. Run the following commands:

For **Linux/macOS**:
```bash
python3 -m venv venv
source venv/bin/activate
```

For **Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install project dependencies

Once your virtual environment is activated, install the required dependencies by running the following command:

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root of your project and add your **Cloudinary** credentials and **database settings**.

Example `.env` file:

```bash
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DBNAME
```

### 5. Run database migrations

To set up your database schema, run the following command to apply all migrations:

```bash
python manage.py migrate
```

### 6. Create a superuser (admin account)

To access the Django admin panel, create a superuser by running the following command:

```bash
python manage.py createsuperuser
```

### 7. Start the development server

Now that everything is set up, you can start the development server by running:

```bash
python manage.py runserver
```

### 8. Access the application

Once the development server is running, open your web browser and go to:

```bash
http://localhost:8000
```

## 🤝 Contributions

Contributions are welcome! If you find a bug, want to suggest a feature, or have an improvement in mind, feel free to open an issue or submit a pull request.

### How to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and write tests if applicable.
4. Ensure that all tests pass.
5. Submit a pull request with a clear description of your changes.

For major changes, please open an issue first to discuss what you would like to change.


