import pytest
from django.contrib.auth.models import User
from restaurants.models import Restaurant, RestaurantOwner


@pytest.mark.django_db
def test_create_restaurant():
    # Create a test user
    test_user = User.objects.create_user(username='testuser', password='testpassword')

    # Create a test restaurant owner
    test_restaurant_owner = RestaurantOwner.objects.create(user=test_user, is_restaurant_owner=True)

    # Create a test restaurant
    test_restaurant = Restaurant.objects.create(
        owner=test_restaurant_owner,
        name='Test Restaurant',
        address='123 Test St',
        phone_number='1234567890',
        description='A test restaurant',
        is_active=True
    )

    # Check if the restaurant is created correctly
    assert test_restaurant.owner == test_restaurant_owner
    assert test_restaurant.name == 'Test Restaurant'
    assert test_restaurant.address == '123 Test St'
    assert test_restaurant.phone_number == '1234567890'
    assert test_restaurant.description == 'A test restaurant'
    assert test_restaurant.is_active is True
