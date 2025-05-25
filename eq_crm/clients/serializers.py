from rest_framework import serializers
from .models import Clients


class ClientSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    unp = serializers.CharField(max_length=18)
    name = serializers.CharField(max_length=180)
    date_add = serializers.DateField(read_only=True)


    def create(self, validated_data):
        return Clients.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.unp = validated_data.get('unp', instance.unp)
        instance.save()
        return instance
