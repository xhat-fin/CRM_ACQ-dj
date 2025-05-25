from django.urls import path
from .views import ClientsAPIView, ClientsAPIViewID

urlpatterns = [
    path('', ClientsAPIView.as_view()),
    path('<int:id>/', ClientsAPIViewID.as_view()),
]
