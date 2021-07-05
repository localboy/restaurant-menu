from django.urls import path
from .views import RestaurantList, UploadMenu


urlpatterns = [
    path('restaurants/', RestaurantList.as_view(), name='restaurants'),
    path('restaurants/upload-todays-menu/', UploadMenu.as_view(), name='upload-todays-menu'),
]