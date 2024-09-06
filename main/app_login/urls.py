# Arquivo que direciona para o views

# Importa
from django.urls import path
from . import views

urlpatterns = [
    # URL do Index
    path('', views.home, name='index'),

    # URL do Sing-In
    path('sign-in/', views.sign_in, name='sign-in'),

    # URL do Sing-Up
    path('sign-up/', views.sign_up, name='sign-up'),

    # URL do Send-Verification
    path('verify-send/', views.verify_send, name='verify-send'),
    path('verify-email/', views.verify_email, name='verify_email'),

    # URL página de Error
    path('error/', views.error, name='error'),
]