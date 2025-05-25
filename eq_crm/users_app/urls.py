
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, CustomTokenObtainPairView, UsersView, UserViewID

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('log-in/', CustomTokenObtainPairView.as_view(), name='login'),
    path('users/', UsersView.as_view(), name='users'),
    path('user/<int:id>', UserViewID.as_view(), name='user'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
