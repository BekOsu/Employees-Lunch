import pytest
from datetime import date
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from menus.models import Menu
from restaurants.models import RestaurantOwner, Restaurant


@pytest.mark.django_db
class TestMenus(APITestCase):

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create test restaurant owner and restaurant
        self.restaurant_owner = RestaurantOwner.objects.create(user=self.user, is_restaurant_owner=True)
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="123 Test St",
            owner=self.restaurant_owner
        )

        # Create an API client and authenticate
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_menu_and_menu_items(self):
        # Create a test Excel file
        excel_content = b'Your excel content'
        excel_file = SimpleUploadedFile("test_excel_file.xlsx", excel_content)

        # Create a menu with an Excel file
        response = self.client.post('/menus/upload/', {'name': 'Test Menu', 'excel_file': excel_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Menu.objects.filter(name='Test Menu').exists())

        # Check the MenuItem objects created from the Excel file
        menu = Menu.objects.get(name='Test Menu')
        # Check if the menu items are created according to the Excel file content

    def test_list_menus(self):
        # Create test menus
        menu1 = Menu.objects.create(restaurant=self.restaurant, name='Test Menu 1')
        menu2 = Menu.objects.create(restaurant=self.restaurant, name='Test Menu 2')

        response = self.client.get('/menus/upload/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_current_day_menu(self):
        # Create a menu for today
        today_menu = Menu.objects.create(restaurant=self.restaurant, name='Today Menu', date=date.today())

        response = self.client.get('/menus/current_day/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Today Menu')
