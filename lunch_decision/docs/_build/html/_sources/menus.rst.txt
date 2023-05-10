Menus App
====================

This section provides an overview of the Menus app in the Lunch Place Decision system.

Introduction
The Menus app is responsible for managing menus and menu items for the restaurants in the Lunch Place Decision system. It allows Restaurant Owners to add and modify their menus for different dates, and also provides functionality for Employees to view the menus and vote for their preferred options.

Usage
Creating a menu: Restaurant Owners can create a new menu by submitting a POST request to the /api/v1/menus/ endpoint with the appropriate data. They can specify the restaurant ID, the date for the menu, and the menu items.

Updating a menu: Restaurant Owners can update an existing menu by submitting a PUT request to the /api/v1/menus/{menu_id}/ endpoint with the updated data. They can modify any of the fields in the menu.

Deleting a menu: Restaurant Owners can delete an existing menu by submitting a DELETE request to the /api/v1/menus/{menu_id}/ endpoint.

Viewing menus: Employees can view the menus for a specific date by submitting a GET request to the /api/v1/menus/?date={date} endpoint, where date is the desired date in YYYY-MM-DD format.

Voting for a menu: Employees can vote for their preferred menu items by submitting a POST request to the /api/v1/menus/vote/ endpoint. In the old version (v1) of the API, they can only vote for one menu item with 3 points. In the new version (v2), they can vote for up to three menu items and allocate points based on their preference (3 points for the top item, 2 points for the second, and 1 point for the third).

Endpoints
/api/v1/menus/: Allows CRUD operations on menus.

/api/v1/menus/vote/: Allows employees to vote for menu items.

Models
Menu: Represents a menu in the system. Includes fields for the restaurant ID, the date, and the menu items.

MenuItem: Represents a single item in a menu. Includes fields for the name, description, and price.

Permissions
Restaurant Owner: Can create, read, update, and delete menus for their own restaurant.

Employee: Can read menus and vote for menu items.