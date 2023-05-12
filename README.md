# employees-lunch

# **lunch_decision App**

This Django application provides an internal service for employees to vote for lunch places. Restaurants can upload their daily menus, and employees can vote on their preferred options. The application supports both old and new mobile app versions, with different voting systems.

## **Table of Contents**

1. Features
2. Installation
3. Running the Application
4. API Documentation
5. Tests
6. HA Cloud Architecture Schema/Diagram.

## **Features**

- Registration and authentication for employees, restaurant owners, and administrators (Both Basic Auth and JWT can be used for authentication).
- Restaurant management (create, list)
- Menu management (create, list daily menus)
- Employee management (create, list)
- Voting system (different behaviors for old and new app versions)
- Containerization (Docker)


## **Installation**

1. Clone the repository:

```
git clone https://github.com/BekOsu/employees-lunch.git

```

2. Start the application using Docker Compose:

```
Run docker-compose build to build the Docker images.
Run docker-compose up to start the development server.

```

## Technology Stack & Features:
* Django fresh build
* RestFramework
* open API and swagger.
* docker with Docker compose.
* kubernetes.
* makefile.
* Logs.
* Schedule Tasks (Django Q) 
* Custom exception handler
* CI/CD Pipeline.
* Linting and Static typing tools.

### **Pre-commit Hooks**

This project uses pre-commit hooks to ensure code quality and consistency. The following hooks are used:

- **`flake8`**
- **`isort`**
- **`black`**
- **`pylint_regular`**
- **`pylint_unittest`**
- **`sort-simple-yaml`**
- **`check-added-large-files`**
- **`check-case-conflict`**
- **`check-symlinks`**
- **`requirements-txt-fixer`**
- **`trailing-whitespace`**
- **`end-of-file-fixer`**
- **`debug-statements`**
- **`fix-encoding-pragma`**
- **`mixed-line-ending`**
- **`add-trailing-comma`**

## CI/CD:
#### Two steps: Build with tests, then Deploy.
#### I commented the part of pushing the images to DockerHub then uploading it to the cloud but, you can easily uncomment that to make it work.
![Screenshot from 2023-05-11 00-58-37](https://github.com/BekOsu/employees-lunch/assets/95960598/71ec17b9-6daa-493a-ad97-87da9e8497e0)


## **API Endpoints**

### **Authentication Endpoints**

- **`POST /user/api/token/`**: Get an access token by providing valid credentials.
- **`POST /user/api/token/refresh/`**: Refresh an existing access token.

### **Restaurant Endpoints**

- **`POST /restaurants/owners/`**: Create a new restaurant owner.
- **`POST /restaurants/ListCreate/`**: Create a new restaurant.
- **`GET /restaurants/ListCreate/`**: Retrieve a list of all restaurants.
- **`GET /restaurants/{id}/`**: Retrieve a specific restaurant by ID.
- **`PUT /restaurants/detail/{id}/`**: Update a specific restaurant by ID.
- **`DELETE /restaurants/detail/{id}/`**: Delete a specific restaurant by ID.

### **Menu Endpoints**

- **`POST /menus/`**: Create a new menu.
- **`GET /menus/`**: Retrieve a list of all menus.
- **`GET /menus/{id}/`**: Retrieve a specific menu by ID.
- **`PUT /menus/{id}/`**: Update a specific menu by ID.
- **`DELETE /menus/{id}/`**: Delete a specific menu by ID.
- **`GET /menus/current_day/`**: Retrieve a current day menus.

### **Menu Endpoints**

- **`POST /employees/account/`**: Create a new employee user.

### **Vote Endpoints**

## **API Versions**

There are two versions of the API available:

### **v1**

The v1 API only allows employees to vote for one restaurant and give it 3 points.

### **v2**

The v2 API allows employees to vote for up to three restaurants and allocate points
to each restaurant based on their preference (3 points for the top restaurant, 2 points
for the second, and 1 point for the third).

- **`POST /employees/votes/`**: Create a new vote using the old voting API.
- **`POST /employees/votes/`**: Create a new vote using the new voting API.
- **`GET /employees/api/today-top-menus/`**: Retrieve a list of all votes.


## **API Documentation**

API documentation is available at **`http://127.0.0.1:8000/swagger/`**.

This provides a detailed overview of the available API endpoints, including their input and output formats.

![Screenshot from 2023-05-11 01-02-56](https://github.com/BekOsu/employees-lunch/assets/95960598/183e4b9a-f107-4b28-ad63-1071007f5725)

## **Sphinx Documentation**

To access the documentation for this project, please go to http://localhost:63342/employees-lunch/docs/_build/html/index.html?_ijt=7ne25me1j1ts1216blrsnv95el
The documentation is generated using Sphinx and covers User Authentication, Restaurants, Menus, and Employee API endpoints.

The HTML pages are in:
 ** /docs/_build/html **.

## **Tests**

To run the test suite, execute the following command:

```
bashCopy code
python manage.py test

```

## **Application Logic**

1. Restaurants can upload their daily menus via the **`/restaurants/`** and **`/menus/`** endpoints.
2. Employees can be created and managed via the **`/employees/`** endpoint.
3. The daily menus for all restaurants can be retrieved using the **`/menus/current_day/`** endpoint, filtered by date.
4. Employees can vote for their preferred lunch options using the **`/employees/votes/`** endpoint.
    - For old app versions, employees can vote for only one restaurant, giving it 3 points.
    - For new app versions, employees can vote for their top three restaurants, assigning them 3, 2, and 1 points, respectively.
5. The voting results for the current day can be retrieved using the **`/employees/api/today-top-menus/`** endpoint, which returns the aggregated points for each restaurant.

Please refer to the API documentation for more details on the usage of each endpoint.

## **HA Cloud Architecture overview:**

                                    ┌───────────────┐
                                    │   Frontend    │
                                    │  (Mobile App) │
                                    └───────────────┘
                                           │
                                           ▼
                                    ┌───────────────┐
                                    │     API       │
                                    │   Gateway     │
                                    └───────────────┘
                                           │
                                           ▼
                                    ┌───────────────┐
                                    │    Backend    │
                                    │    Server     │
                                    └───────────────┘
                                           │
                           ┌───────────────┴───────────────┐
                           ▼                               ▼
               ┌───────────────────────┐        ┌───────────────────────┐
               │    Django Rest        │        │   Menu Management     │
               │   Framework Views     │        │       Service         │
               └───────────────────────┘        └───────────────────────┘
                            │                               │
                            ▼                               ▼
               ┌───────────────────────┐        ┌───────────────────────┐
               │  Authentication       │        │   Vote Management     │
               │       Service         │        │       Service         │
               └───────────────────────┘        └───────────────────────┘
                            │                               │
                            ▼                               ▼
               ┌───────────────────────┐        ┌───────────────────────┐
               │     Data Management   │        │     External APIs     │
               │       Service         │        │                       │
               └───────────────────────┘        └───────────────────────┘

This is an overview of the architecture for the internal service, which enables employees to make decisions on lunch
places. The service consists of the following components:

- **Frontend**: Represents the mobile app used by employees to interact with the service.
- **API Gateway**: Acts as a central entry point for requests, handling routing, security, and versioning.
- **Backend Server**: Responsible for handling the business logic and processing requests from the API Gateway.
- **Django Rest Framework Views**: Implements API endpoints and handles incoming requests.
- **Authentication Service**: Manages user authentication and permissions.
- **Menu Management Service**: Handles restaurant menus, including upload, retrieval, and storage.
- **Vote Management Service**: Handles employee voting for menus and aggregation of votes.
- **Data Management Service**: Manages data related to the service, including validation, storage, and access.
- **Database Storage**: Utilizes Azure Blob Storage or similar service for additional data storage.
- **External APIs**: Allows integration with external services for additional functionalities or data access.

This architecture follows a client-server model, with the mobile app as the client and the backend server handling
the business logic. The API Gateway ensures secure and efficient request handling, and various services manage specific
functionalities, such as authentication, menu management, and data storage.

## **Future Work:**
Explore additional features like user suggestions and detailed restaurant information, and incorporate technologies 
such as Django signals, Redis, Celery, scheduled tasks, custom exception handling, message broker (Kafka, RabbitMQ), 
Nginx API gateway, service registry (e.g., Eureka), notification service, 
and design patterns (Pub-Sub, Adapter, Factory, Singleton).

## **Contributors**

- Abubaker Suliman

## **License**

This project is licensed under the MIT License - see the LICENSE.md file for details.