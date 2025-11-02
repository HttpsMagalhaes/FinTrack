from django.shortcuts import render
from django.core.cache import cache
from .models import Acao
from .utils import get_stock_data
import datetime
import yfinance as yf

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
    acoes = Acao.objects.exclude(nome_empresa__iexact="Desconhecido").order_by('nome_empresa')
    dados_acoes = []

    for acao in acoes:
        try:
            ticker = yf.Ticker(acao.ticket)
            info = ticker.history(period="7d")  # últimos dois dias
            if len(info) >= 2:
                preco_ontem = info['Close'][-7]
                preco_semana = info['Close'][-1]
                variacao = ((preco_semana - preco_ontem) / preco_ontem) * 100
            else:
                variacao = None
        except Exception as e:
            print(f"Erro ao buscar dados de {acao.ticket}: {e}")
            variacao = None

        dados_acoes.append({
            'ticket': acao.ticket,
            'nome_empresa': acao.nome_empresa,
            'setor': acao.setor,
            'variacao': variacao,
        })

    return render(request, 'lista_rentaveis.html', {'acoes': dados_acoes})
