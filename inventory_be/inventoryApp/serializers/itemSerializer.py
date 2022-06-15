from rest_framework import serializers
from inventoryApp.models.item import Item
from drf_extra_fields.fields import Base64ImageField


class ItemSerializer(serializers.ModelSerializer):
    evidence = Base64ImageField(required=False)
    class Meta:
        model = Item
        fields = ['id', 'name', 'evidence']
    