from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contato/', views.contato, name='contato'),
    path('comparacao/', views.comparacao, name='comparacao'),
    path('favoritos/', views.favoritos, name='favoritos'),
    path('perfil/', views.perfil, name='perfil'),
    path('lista_rentaveis/', views.lista_rentaveis, name='lista_rentaveis'),
    path('top10/', views.top10_rentaveis, name='top10_rentaveis'),
]

