from rest_framework import serializers
from inventoryApp.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User   #modelo que se va a usar
        fields = ['id', 'name','email', 'password', 'is_admin', 'is_client']  #claves que se quieren usar, adicional la cuenta, para conocer los datos de la cuenta asosciada a ese usario

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
        
