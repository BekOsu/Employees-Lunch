Employee App
====================

Introduction
This documentation outlines the available endpoints and functionality for the Employee API.

Getting Started
To use the Employee API, you will need to have an employee account created in the Lunch Place Decision app. Once you have your login credentials, you can access the following endpoints.

Endpoints
GET /api/employee/menus/{date}/

bash
Copy code

Returns the menus for a specific date.

- `date` (required): The date to retrieve menus for in the format `YYYY-MM-DD`.

Example Response:

```json
[
  {
    "id": 1,
    "restaurant": {
      "id": 1,
      "name": "Joe's Pizza",
      "address": "123 Main St"
    },
    "date": "2023-05-10",
    "items": "Pizza, Salad, Breadsticks"
  },
  {
    "id": 2,
    "restaurant": {
      "id": 2,
      "name": "Sushi Palace",
      "address": "456 Maple Ave"
    },
    "date": "2023-05-10",
    "items": "Sushi, Miso Soup, Seaweed Salad"
  }
]
```

POST `/api/employee/votes/{version}/`
Allows an employee to vote for a menu.

version (required): The API version to use for voting (v1 or v2).
employee (optional): The ID of the employee submitting the vote. Defaults to the currently authenticated user.
votes (required): A list of up to 3 dictionaries, each representing a restaurant and the number of points to allocate to it.
Example Request:

json
Copy code
{
  "votes": [
    {
      "restaurant_id": 1,
      "points": 3
    },
    {
      "restaurant_id": 2,
      "points": 2
    },
    {
      "restaurant_id": 3,
      "points": 1
    }
  ]
}
Example Response:

json
Copy code
{
  "id": 1,
  "employee": {
    "id": 1,
    "username": "johndoe",
    "email": "johndoe@example.com"
  },
  "menu": {
    "id": 1,
    "restaurant": {
      "id": 1,
      "name": "Joe's Pizza",
      "address": "123 Main St"
    },
    "date": "2023-05-10",
    "items": "Pizza, Salad, Breadsticks"
  },
  "points": 3
}
Conclusion
The Employee API provides functionality for retrieving menus for a specific date and submitting votes for those menus. By using the endpoints provided in this documentation, employees can efficiently make decisions about where to eat for lunch.