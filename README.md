# **Reach App**

Reach App is a Django-based project for managing and documenting a social media-like platform. It includes backend functionality for posts, comments, and likes, as well as frontend templates. The project is fully documented using Swagger and MkDocs for API and project-level documentation.

---

## **Features**
- User authentication and session management.
- CRUD operations for posts, comments, and likes.
- Real-time notifications for user actions.
- API documentation with **Swagger UI** and **Redoc**.
- Project documentation using **MkDocs**.

---

## **Installation**

### **1. Clone the Repository**

### git clone https://github.com/Mohamed-Tarek-MT/Reach-App.git
### cd Reach-App
### 2. Set Up the Virtual Environment
### Create and activate a virtual environment:

### python -m venv .venv
### .\.venv\Scripts\activate  # Windows
### source .venv/bin/activate  # macOS/Linux
### 3. Install Dependencies
### Install the required packages:

### pip install -r requirements.txt
### Configuration
### 1. Database
### By default, the project uses SQLite. To migrate the database:

### python manage.py makemigrations
### python manage.py migrate

# 2. Static and Media Files
### Ensure static and media files are properly served during development:

### python manage.py collectstatic

### Usage
### 1. Run the Development Server

# Start the Django server:
### python manage.py runserver

Access the app at:

-Frontend: (http://127.0.0.1:8000/)
-Admin Panel: (http://127.0.0.1:8000/admin/)
#2. API Documentation
-Swagger UI: (http://127.0.0.1:8000/swagger/)
-Redoc: (http://127.0.0.1:8000/redoc/)
#3. MkDocs Documentation

# Serve the project documentation:
-mkdocs serve

#Access it at:
- (http://127.0.0.1:8000/)

#Testing
## 1. Using Postman
-Import the Swagger JSON from (http://127.0.0.1:8000/swagger/) into Postman to test endpoints interactively.

## 2. Example CURL Request
-To fetch all posts:

- curl (http://127.0.0.1:8000/posts/)

# Project Structure

### api/                 - Backend app containing views, models, serializers, and APIs
###  docs/               - MkDocs documentation files
###  static/             - Static assets (CSS, JS, images)
###  templates/          - HTML templates for frontend
###  manage.py           - Django management script
###  requirements.txt    - Python dependencies
###  README.md           - Project documentation
