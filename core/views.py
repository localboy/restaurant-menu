import xlrd
from django.utils import timezone
from rest_framework import generics, permissions, views, response, status

from .models import Restaurant, Menu
from .serializers import RestaurantSerializer

xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True


class RestaurantList(generics.ListCreateAPIView):
    """
    GET : Allow user to get list of restaurants
    POST : Allow user to create restaurant
    """
    queryset =  Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]


class UploadMenu(views.APIView):
    """
    POST: Allow user to upload todays menu.
    A sample excel file is added to the project root directoy.
    """

    def post(self, request, format=None):
        try:
            file_obj = request.FILES['file'].temporary_file_path()
            wb = xlrd.open_workbook(file_obj)
            sheet = wb.sheet_by_index(0)
            total_restaurant = 0
            total_menu = 0
            
            for i in range(sheet.nrows):
                restaurant_name = sheet.row_values(i)[0].strip()
                menu_name = sheet.row_values(i)[1].strip()
                menu_desc = sheet.row_values(i)[2].strip()
                restaurant, created = Restaurant.objects.get_or_create(name=restaurant_name)
                if created:
                    total_restaurant += 1
                menu = Menu.objects.create(
                    restaurant=restaurant, 
                    name = menu_name, 
                    description=menu_desc, 
                    date=timezone.now().date()
                    )
                total_menu += 1

            return response.Response({'total_restaurant': total_restaurant, 'total_menu': total_menu}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return response.Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
