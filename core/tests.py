from core.serializers import MenuSerializer
from datetime import date, time
import os
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from rest_framework import response, status
from rest_framework.test import APIClient

from core.models import Employee, Restaurant, Menu
from mylunch.settings import BASE_DIR


def get_api_url(url):
    """ Return full API URL: (partial_url) """
    return u"/api/v1/{}/".format(url)


class MyLunchTestCase(TestCase):

    def assertSuccess(self, request):
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def assertCreated(self, request):
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def assertDeleted(self, request):
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def assertBadRequest(self, request):
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def assertForbidden(self, request):
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def assertNotFound(self, request):
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)



class MyLunchAPITEST(MyLunchTestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User(username='testuser', email='test@gmail.com')
        self.user.set_password('secret')
        self.user.save()

        self.employee = Employee.objects.create(user=self.user, designation='Manager', phone='435345434')

        self.client.login(username='testuser', password='secret')

        self.restaurant = Restaurant.objects.create(name='test restaurant')
        self.menu1 = Menu.objects.create(
            restaurant=self.restaurant, 
            name='test menu', 
            description='Menu description', 
            date=timezone.now().date()
        )

        self.current_date = timezone.now().date()
        self.yesterday = self.current_date - timezone.timedelta(days=1)
        self.the_day_before_yesterday = self.current_date - timezone.timedelta(days=2)

    def test_create_restaurant(self):
        response = self.client.post(get_api_url('restaurants'), {'name':'Test Restaurant'})
        self.assertCreated(response)

    def test_get_restaurants_list(self):
        response = self.client.get(get_api_url('restaurants'))
        self.assertSuccess(response)

    def test_upload_menu(self):
        menu_file = os.path.join(BASE_DIR, 'menu-list.xlsx')
        data = File(open(menu_file, 'rb'))

        file = SimpleUploadedFile(menu_file, data.read(), content_type='multipart/form-data')
        payload = {"file": file}
        response = self.client.post(
            get_api_url('restaurants/upload-todays-menu'), payload, format="multipart")
        
        self.assertCreated(response)

    def test_get_employee_list(self):
        response = self.client.get(get_api_url('employees'))
        self.assertSuccess(response)

    def test_create_employee(self):
        data = {
            'user':{
                'first_name': 'Firstname',
                'last_name': 'Lastname',
                'username':'testemployee',
                'email': 'testemployee@gmail.com',
                'password': 'secrete',
                },
            'phone': '01731736326',
            'designation':'Accountant'
            }
        response = self.client.post(get_api_url('employees'), data, format='json')
        self.assertCreated(response)

    def test_todays_menu(self):
        restaurant = Restaurant.objects.create(name='Restaurant 2')
        menu = Menu.objects.create(
            restaurant=restaurant, 
            name="Menu 2", 
            description='Menu description', 
            date=self.yesterday
            )
        another_nemu = Menu.objects.create(
            restaurant=restaurant, 
            name="Another Menu", 
            description='Menu description', 
            date=self.current_date
            )
        response = self.client.get(get_api_url('restaurants/todays-menu'))
        self.assertSuccess(response)
        self.assertEqual(len(response.data), 2)
