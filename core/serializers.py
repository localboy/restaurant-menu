from django.contrib.auth.models import User
from django.db import transaction

from rest_framework import serializers

from .models import Restaurant, Employee, Menu


class UserBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class UserWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password')


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer()

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeWriteSerializer(serializers.ModelSerializer):
    user = UserWriteSerializer()

    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data):
        with transaction.atomic():
            try:
                user = User.objects.get(username=validated_data['user']['username'])
                user.first_name = validated_data['user']['first_name']
                user.last_name = validated_data['user']['last_name']
                user.email = validated_data['user']['email']
                user.set_password(validated_data['user']['password'])
                user.save(update_fields=['email', 'password'])

                employee, created = Employee.objects.get_or_create(
                    user=user, phone=validated_data['phone'], 
                    designation=validated_data['designation']
                    )
            except User.DoesNotExist:
                user = User(
                    username=validated_data['user']['username'],
                    first_name = validated_data['user']['first_name'],
                    last_name = validated_data['user']['last_name'],
                    email=validated_data['user']['email'])
                user.set_password(validated_data['user']['password'])
                user.save()
                employee = Employee.objects.create(
                    user=user, 
                    phone=validated_data['phone'], 
                    designation=validated_data['designation']
                    )
            return employee


class MenuSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()

    class Meta:
        model = Menu
        exclude = ('votes', )
