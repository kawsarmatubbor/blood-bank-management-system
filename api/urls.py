from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('registration/', views.RegistrationViewSet.as_view(), name='registration'),
    path('verification/<str:token>/', views.verification_view, name='verification'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('logout/', views.logout_view, name='logout'),
]