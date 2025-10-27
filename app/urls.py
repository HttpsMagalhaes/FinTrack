from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contato/', views.contato, name='contato'),
    path('comparacao/', views.comparacao, name='comparacao'),
    path('favoritos/', views.favoritos, name='favoritos'),
    path('perfil/', views.perfil, name='perfil'),
    path('rentaveis/', views.rentaveis, name='rentaveis'),
]
