# Arquivo que direciona para o views

# Importa
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.cloud_index, name='cloud_index'),  # Defina a URL com um nome
]