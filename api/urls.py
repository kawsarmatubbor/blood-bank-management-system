from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.RegistrationViewSet.as_view(), name='registration'),
    path('verification/<str:token>/', views.verification_view, name='verification'),
]