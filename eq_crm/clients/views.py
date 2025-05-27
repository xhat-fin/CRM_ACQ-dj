from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from .models import Clients
from .serializers import ClientSerializer


class ClientsAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        clients = Clients.objects.all()
        return Response(ClientSerializer(clients, many=True).data)


    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"new_clients": serializer.data})



class ClientsAPIViewID(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        client = Clients.objects.get(id=id)
        serializer = ClientSerializer(client)
        return Response(serializer.data)


    def put(self, request, **kwargs):
        id = kwargs.get('id')
        try:
            instance = Clients.objects.get(id=id)
        except:
            return Response({"error": "client not exists"})

        serializer = ClientSerializer(data=request.data, instance=instance, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response({"clients": serializer.data})

