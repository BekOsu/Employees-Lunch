from django.contrib.auth.models import User
from employee.models import Employee
from restaurants.models import RestaurantOwner


def test_create_restaurant_owner():
    # Create a test user
    test_user = User.objects.create_user(username='testuser', password='testpassword')

    # Create a test restaurant owner
    test_restaurant_owner = RestaurantOwner.objects.create(user=test_user, is_restaurant_owner=True)

    # Assert the test user and restaurant owner have been created
    assert User.objects.count() == 1
    assert RestaurantOwner.objects.count() == 1
    assert test_restaurant_owner.user == test_user
    assert test_restaurant_owner.is_restaurant_owner is True


def test_create_employee_user():
    # Create a test user
    test_user = User.objects.create_user(username='testemployee', password='testpassword')

    # Create a test employee
    test_employee = Employee.objects.create(user=test_user, is_employee=True)

    # Assert the test user and employee have been created
    assert User.objects.count() == 1
    assert Employee.objects.count() == 1
    assert test_employee.user == test_user
    assert test_employee.is_employee is True
