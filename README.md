# Trails Management API
The **Trails Management API** is a project designed to manage trails, their features, and user data through a RESTful API implemented using Flask and SQLAlchemy. This API includes role-based authentication, CRUD operations for trails and features, and integrates Swagger for user-friendly API documentation.
## Table of Contents
- [Overview]()
- [Features]()
- [Project Structure]()
- [Technology Stack]()
- [Installation]()
- [Usage]()
- [API Endpoints]()
- [Testing]()
- [Security Best Practices]()
- [Future Improvements]()
- [Author]()

## Overview
This API provides database management functionalities for trails through secure endpoints. It offers various CRUD operations while enforcing role-based access controls to allow precise user and admin functionality.
### Objectives
1. Efficient trail management via a modular database.
2. Secure user data adhering to GDPR standards.
3. Ease of use through Swagger and Docker integration.

## Features
- **User Authentication:**
    - Role-based user access control (User/Admin).
    - JWT-based (encrypted using a Fernet key) role authorization.
    - Login and logout functionality to manage session states.

- **CRUD Operations** for:
    - **Trails**: Manage trail details such as name, location, difficulty, etc.
    - **Features**: Add and manage features (e.g., mountain views, waterfalls).
    - **Trail Locations**: Points on a trail defined by latitude/longitude.

- **Swagger Integration**:
    - User-friendly interface for testing and interaction with API endpoints.

- **Testing**:
    - Comprehensive test suite for API endpoints and role-based access validation.

## Project Structure
``` plaintext

├──Templates
|  └── home.html             # MAin page 
├── app.py                  # Main entry point for the API
├── config.py               # Database and app configurations
├── models.py               # ORM models for database interaction
├── trails.py               # CRUD functions for trail management
├── Features.py             # CRUD functions for trail features
├── authenticator.py        # Authentication functions
├── token_checker.py        # Token-based role validation
├── testing.py              # Includes unit tests for validating endpoints
├── requirements.txt        # Application dependencies
├── Dockerfile              # Configuration for Docker container
├── swagger.yml             # API documentation in OpenAPI format
└── README.md               # This...
```
## Technology Stack
- **Programming Language**: Python
- **Frameworks**: Flask, Connexion
- **Database**: SQLAlchemy with MS SQL Server (Transact)
- **API Documentation**: Swagger with YAML
- **Uploaded to**: Docker
- **Testing**: Pytest

## Installation
### Prerequisites:
- Install Docker.
- Python version 3.9 or higher.

### Steps:
1. Clone the repository:
``` bash
   git clone https://github.com/Jakelr26/COMP2001-Trail-API.git
   cd COMP2001-Trail-API
```
1. Install dependencies:
``` bash
   pip install -r requirements.txt
```
1. Configure the database connection in `config.py`.
2. Build the Docker image:
``` bash
   docker build -t trails-api .
```
1. Run the Docker container:
``` bash
   docker run -p 8000:8000 trails-api
```
1. Access the API at:
    - Swagger UI: `http://localhost:8000/api/ui/`
    - Home Page: `http://localhost:8000/`
    - (homepage has button to UI)

## Usage
### Authenticating Users:
- Use the `/login` endpoint to obtain an encrypted token by providing valid `email` and `password`.
- Role tokens are automatically stored in `permissions.json`.

### CRUD Operations:
- Use Swagger UI to interact with various endpoints to create, read, update, or delete trails, features, and locations.

## API Endpoints
Key endpoints available in the API:

| Endpoint | Method | Description | Role Required |
| --- | --- | --- | --- |
| `/login` | POST | Authenticate users | - |
| `/logout` | GET | Logout to clear session data | - |
| `/api/trails` | GET | Retrieve all trails | User/Admin |
| `/api/trails` | POST | Add a new trail | Admin |
| `/api/features` | GET | Retrieve all features of trails | User/Admin |
| `/api/features/{id}` | PUT | Update an individual feature | Admin |
| `/` | GET | Displays the home page with trails | User/Admin |
Refer to the Swagger UI for complete API documentation.
## Testing
The project includes a comprehensive suite of tests implemented in **`test_the_app.py` **. Tools used:
- **Pytest** framework for validating API endpoints, edge cases, and permissions.
- Tests include:
    - Validating roles and token authorization.
    - CRUD operation successes and failures handling.

Run tests with:
``` bash
pytest test_the_app.py
```
## Security Best Practices
- **HTTPS (futre)**:
    - Ensures secure data transit by encrypting all requests.

- **Role-based Access Control**:
    - Admin and User roles strictly defined.

- **Encryption of Sensitive Data**:
    - User tokens encrypted using **Fernet**.

## Future Improvements
1. **UI Development**:
    - A full web interface with HTML/CSS to enhance usability and visual appeal.

2. **Backend Enhancements**:
    - Implement stricter CSRF protection.
    - Add testing validation for more edge cases.
    - add proper JWTs (like what I attempted)

3. **Deployment**:
    - Full cloud-based deployment with HTTPS configured.

## Author
- **Jake Lear**
    - COMP2001 Coursework Project - **Trails API**
    - [GitHub Repository]()
