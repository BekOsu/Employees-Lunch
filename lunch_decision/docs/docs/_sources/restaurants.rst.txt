Restaurants App
====================

Introduction
This documentation outlines the Restaurants API of the Lunch Place Decision app. It explains the different endpoints available and the parameters that can be used to make requests.

Endpoints
The following endpoints are available in the Restaurants API:

GET /restaurants/: Retrieves a list of all restaurants.
POST /restaurants/: Creates a new restaurant.
GET /restaurants/{restaurant_id}/: Retrieves details for a specific restaurant.
PUT /restaurants/{restaurant_id}/: Updates a specific restaurant.
DELETE /restaurants/{restaurant_id}/: Deletes a specific restaurant.
Parameters
When making requests to the Restaurants API, the following parameters can be used:

name: The name of the restaurant.
address: The address of the restaurant.
phone_number: The phone number of the restaurant.
website: The website URL of the restaurant.
owner: The ID of the Restaurant Owner who owns the restaurant.
Permissions
To access the Restaurants API, a user must be authenticated as a Restaurant Owner. This means that they must have an account with the is_restaurant_owner flag set to True.

Examples
The following examples show how to make requests to the Restaurants API:

To retrieve a list of all restaurants:
bash
Copy code
GET /restaurants/
To create a new restaurant:
bash
Copy code
POST /restaurants/

{
    "name": "Example Restaurant",
    "address": "123 Main St",
    "phone_number": "555-1234",
    "website": "https://www.example.com/",
    "owner": 1
}
To retrieve details for a specific restaurant:
bash
Copy code
GET /restaurants/1/
To update a specific restaurant:
bash
Copy code
PUT /restaurants/1/

{
    "name": "Updated Restaurant Name",
    "address": "456 Main St",
    "phone_number": "555-5678",
    "website": "https://www.updated-example.com/",
    "owner": 1
}
To delete a specific restaurant:
bash
Copy code
DELETE /restaurants/1/