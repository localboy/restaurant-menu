from django.urls import path
from .views import RestaurantList


urlpatterns = [
    path('restaurants/', RestaurantList.as_view(), name='restaurants'),
]