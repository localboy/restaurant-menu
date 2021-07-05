from django.urls import path
from .views import EmployeeList, RestaurantList, UploadMenu, TodaysMenu


urlpatterns = [
    path('employees/', EmployeeList.as_view(), name='employees'),
    path('restaurants/', RestaurantList.as_view(), name='restaurants'),
    path('restaurants/todays-menu/', TodaysMenu.as_view(), name='todays-menu'),
    path('restaurants/upload-todays-menu/', UploadMenu.as_view(), name='upload-todays-menu'),
]