from rest_framework import serializers
from inventoryApp.models.employee import Employee
from drf_extra_fields.fields import Base64ImageField


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name']
    