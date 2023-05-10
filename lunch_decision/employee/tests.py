import pytest
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from employee.models import Employee, Vote
from menus.models import Menu, MenuItem
from restaurants.models import Restaurant


@pytest.mark.django_db
class TestEmployeeAndVoting(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='employee', password='password123')
        self.employee = Employee.objects.create(user=self.user, company='Company', department='Department')

        # Create restaurant, menu and menu items
        self.restaurant = Restaurant.objects.create(name='Test Restaurant', owner=self.employee)
        self.menu = Menu.objects.create(restaurant=self.restaurant, name='Test Menu')
        self.menu_item1 = MenuItem.objects.create(name='Menu item 1', price=10, menu=self.menu)
        self.menu_item2 = MenuItem.objects.create(name='Menu item 2', price=12, menu=self.menu)
        self.menu_item3 = MenuItem.objects.create(name='Menu item 3', price=15, menu=self.menu)

        # Authenticate the user
        self.client.login(username='employee', password='password123')

    def test_create_employee(self):
        user_data = {
            'username': 'test_employee',
            'email': 'test_employee@example.com',
            'password': 'testpassword',
        }
        data = {
            'user': user_data,
            'company': 'Test Company',
            'department': 'Test Department'
        }
        response = self.client.post('/employees/account', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Employee.objects.filter(user__username='test_employee').exists())

    def test_create_vote(self):
        data = {'menu': self.menu_item1.id}
        response = self.client.post('/employees/votes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Vote.objects.filter(employee=self.employee, menu=self.menu_item1).exists())

    def test_today_top_menus(self):
        # Create votes for menu items
        Vote.objects.create(employee=self.employee, menu=self.menu_item1, points=3)
        Vote.objects.create(employee=self.employee, menu=self.menu_item2, points=2)
        Vote.objects.create(employee=self.employee, menu=self.menu_item3, points=1)

        response = self.client.get('/employees/api/today-top-menus/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Ensure there are 3 top menus returned
        self.assertEqual(response.data[0]['id'], self.menu_item1.id)
        self.assertEqual(response.data[1]['id'], self.menu_item2.id)
        self.assertEqual(response.data[2]['id'], self.menu_item3.id)
