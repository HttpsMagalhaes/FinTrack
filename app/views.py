from django.shortcuts import render
from .models import Acao
from .utils import get_stock_data

def home(request):
    return render(request, 'index.html', {'template_name': 'home.html'})

def comparacao(request):
    return render(request, 'index.html', {'template_name': 'comparacao.html'})

def favoritos(request):
    return render(request, 'index.html', {'template_name': 'favoritos.html'})

def contato(request):
    return render(request, 'index.html', {'template_name': 'contato.html'})

def perfil(request):
    return render(request, 'index.html', {'template_name': 'perfil.html'})

def lista_rentaveis(request):
    return render(request, 'index.html', {'template_name': 'lista_rentaveis.html'})

