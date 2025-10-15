import yfinance as yf
from django.shortcuts import render

def olamundo(request):
    # Agora, em vez de texto, renderizamos o template
    return render(request, 'index.html')