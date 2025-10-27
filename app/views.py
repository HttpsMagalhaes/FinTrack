
from django.shortcuts import render

def home(request):
    # Agora, em vez de texto, renderizamos o template
    return render(request, 'index.html')

def pagina_contato(request):
    # Simplesmente renderiza o template 'contato.html'
    return render(request, 'contato.html')