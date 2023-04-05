from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import RegisterAPIView, AuthAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("auth/", AuthAPIView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()),
]