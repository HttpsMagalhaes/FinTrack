from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('buscar/', views.buscar_acao, name='buscar_acao'),
    path('comparacao/', views.comparacao, name='comparacao'),
    path('lista_rentaveis/', views.lista_rentaveis, name='lista_rentaveis'),
    path('acao/<str:ticket>/', views.detalhes_acao, name='detalhes_acao'),
    path('favoritos/', views.favoritos, name='favoritos'), 

    # Rota para ver a LISTA (Menu "Favoritos") - Não pede ticket
    path('favoritos/', views.favoritos, name='favoritos'),
    # Rota para a AÇÃO (Clicar no coração) - Pede ticket. 
    path('favoritar/<str:ticket>/', views.favoritar_acao, name='favoritar_acao'),

    #Login
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
]

