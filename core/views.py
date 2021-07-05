from rest_framework import generics, permissions

from .models import Restaurant
from .serializers import RestaurantSerializer

class RestaurantList(generics.ListCreateAPIView):
    """
    GET : Allow user to get list of restaurants
    POST : Allow user to create restaurant
    """
    queryset =  Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]
