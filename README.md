# eCommerce Backend

This is an eCommerce backend application built using FastAPI. It provides a RESTful API for managing products and users in an eCommerce platform.

## Project Structure

```
ecommerce-backend
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── endpoints
│   │   │   ├── __init__.py
│   │   │   └── products.py
│   │   │   └── users.py
│   ├── core
│   │   ├── __init__.py
│   │   └── config.py
│   ├── models
│   │   ├── __init__.py
│   │   └── product.py
│   │   └── user.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── product.py
│   │   └── user.py
│   ├── crud
│   │   ├── __init__.py
│   │   └── product.py
│   │   └── user.py
│   └── db
│       ├── __init__.py
│       └── base.py
├── requirements.txt
└── README.md
```

## Features

- User registration and authentication
- Product management (CRUD operations)
- FastAPI for high performance
- Pydantic for data validation

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd ecommerce-backend
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Documentation

The interactive API documentation can be accessed at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## License

This project is licensed under the MIT License.