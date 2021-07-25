import xlrd
from django.utils import timezone
from rest_framework import generics, permissions, views, response, status

from .models import Restaurant, Menu, Employee, Vote
from .serializers import RestaurantSerializer, EmployeeSerializer, \
    EmployeeWriteSerializer, MenuSerializer, VoteSerializer

xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True


class RestaurantList(generics.ListCreateAPIView):
    """
    get : Allow user to get list of restaurants
    post : Allow user to create restaurant
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]


class UploadMenu(views.APIView):
    """
    post: Allow user to upload todays menu.
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
                restaurant, created = Restaurant.objects.get_or_create(
                    name=restaurant_name)
                if created:
                    total_restaurant += 1
                Menu.objects.create(
                    restaurant=restaurant,
                    name=menu_name,
                    description=menu_desc,
                    date=timezone.now().date()
                    )
                total_menu += 1

            return response.Response({
                'total_restaurant': total_restaurant,
                'total_menu': total_menu},
                status=status.HTTP_201_CREATED)
        except Exception as e:
            return response.Response(
                {'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST)


class EmployeeList(generics.ListCreateAPIView):
    """
    get: API endpoint to get list of Employee
    post: API endpoint to create Employee
    """
    queryset = Employee.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EmployeeWriteSerializer
        return EmployeeSerializer


class TodaysMenu(generics.ListAPIView):
    """
    get: Get today's menu list
    """
    serializer_class = MenuSerializer

    def get_queryset(self):
        return Menu.objects.filter(date=timezone.now().date())


class MenuVotting(generics.CreateAPIView):
    """
    post: Vote for Menu
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def post(self, request, menu_id, *args, **kwargs):
        employee = Employee.objects.get(user=self.request.user)
        menu = Menu.objects.get(pk=menu_id)

        serializer = VoteSerializer(data={
            'employee': employee.id, 'menu': menu.id
            })
        if serializer.is_valid(raise_exception=True):
            menu.votes += 1
            menu.save(update_fields=['votes'])
            serializer.save()

        return response.Response(serializer.data, status=status.HTTP_200_OK)


class Winner(views.APIView):
    """
    get: API endpoint to get today's wiiner
    """
    def get(self, request, format=None):
        current_date = timezone.now().date()
        yesterday = current_date - timezone.timedelta(days=1)
        the_day_before_yesterday = current_date - timezone.timedelta(days=2)

        yesterday_winner = Menu.objects.filter(
            date=yesterday).order_by('-votes').first()

        the_day_before_yesterday_winner = Menu.objects.filter(
            date=the_day_before_yesterday).order_by('-votes').first()

        todays_menu = Menu.objects.filter(date=timezone.now().date())

        # Checking if the last two days' winners are the same restaurant.
        # If they are the same then the restaurant will be excluded from today
        if (yesterday_winner and the_day_before_yesterday_winner and
                (yesterday_winner.restaurant.id ==
                    the_day_before_yesterday_winner.restaurant.id)):

            todays_menu = todays_menu.exclude(
                restaurant__id=yesterday_winner.restaurant.id)

        winner = todays_menu.order_by('-votes').first()
        serializer = MenuSerializer(winner)

        return response.Response(serializer.data, status=status.HTTP_200_OK)
