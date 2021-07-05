from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Employee, Restaurant, Menu


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
        self.menu1 = Menu.objects.create(restaurant=self.restaurant, name='test menu', description='Menu description', date=timezone.now().date())

    def test_create_restaurant(self):
        response = self.client.post(get_api_url('restaurants'), {'name':'Test Restaurant'})
        self.assertCreated(response)

    def test_get_restaurants_list(self):
        response = self.client.get(get_api_url('restaurants'))
        self.assertSuccess(response)
