# InternGrow Capstone Project – Inventory Management System

A production-ready Python Flask Inventory Management System developed as part of the InternGrow Capstone Project.

## Project Overview

The Inventory Management System provides a simple and secure way to manage products and inventory records. It includes user authentication, database integration, CRUD operations, REST API endpoints, CSV export, logging, exception handling, and configuration management.

## Features

- User registration and login authentication
- Secure password hashing
- Session-based authentication
- Object-Oriented Programming architecture
- SQLite database integration
- Product CRUD operations
- Dashboard with inventory statistics
- REST API for product management
- CSV inventory export
- Exception handling
- Application logging
- Configuration management
- Responsive web interface

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- SQLite
- HTML
- CSS
- REST API
- Git & GitHub

## Project Structure

Interngrow_CapstoneProject_InventoryManagementSystem/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── api.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── products.html
│   ├── add_product.html
│   └── edit_product.html
│
├── static/
│
├── exports/
├── logs/
├── config.py
├── run.py
├── requirements.txt
├── .gitignore
└── README.md

## Installation

1. Clone the repository

git clone https://github.com/IrsaAttiqueCyber/InternGrow_CapstoneProject_InventoryManagementSystem.git

2. Navigate to the project directory

cd InternGrow_CapstoneProject_InventoryManagementSystem

3. Create a virtual environment

python -m venv venv

4. Activate the virtual environment

Windows PowerShell:
venv\Scripts\activate

5. Install dependencies

pip install -r requirements.txt

6. Run the application

python run.py

The application will be available at:

http://127.0.0.1:5000

## API Endpoints

Get all products

GET /api/products

Create a product

POST /api/products

Example JSON:

{
    "name": "Mouse",
    "category": "Accessories",
    "quantity": 10,
    "price": 1500
}

## Authentication

The system provides:

- User registration
- Secure password hashing
- Login and logout
- Protected inventory management routes

## Database

The application uses SQLite through Flask-SQLAlchemy for storing users and product information.

## File Handling

The system supports exporting inventory records to CSV format.

## Logging

Application activities and errors are recorded in:

logs/app.log

## Exception Handling

The application uses exception handling to manage invalid input, database errors, and other runtime errors while maintaining application stability.

## Configuration

Application configuration is managed through config.py. Environment variables can be used for sensitive configuration such as the secret key and database URL.

## Author

Irsa Attique
InternGrow Capstone Project