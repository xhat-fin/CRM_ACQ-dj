from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .serializers import UserSerializer
from .models import User


# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"user": serializer.data})
        return Response({"error": serializer.errors})


class UsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)


class UserViewID(APIView):

    def get(self, request, id):
        user = User.objects.get(id=id)
        return Response(UserSerializer(user).data)



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer