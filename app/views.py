from django.core.cache import cache
from .models import Acao
import yfinance as yf
import json 
from django.shortcuts import render, redirect
from django.db.models import FloatField
from django.db.models.functions import Cast
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Acao, AcaoFavoritada


def comparacao(request):
    return render(request, 'index.html', {'template_name': 'comparacao.html'})

def favoritos(request):
    return render(request, 'index.html', {'template_name': 'favoritos.html'})

def lista_rentaveis(request):
    # ATUALIZE ESTA LINHA:
    # Adicionamos .exclude(ticket='') para ignorar ações sem código
    acoes = Acao.objects.exclude(nome_empresa__iexact="Desconhecido").exclude(ticket__exact='').exclude(ticket__isnull=True).order_by('nome_empresa')
    
    dados_acoes = []

    for acao in acoes:
        try:
            # Dica extra: Se o ticket não tiver .SA, adicionamos aqui para evitar erro no Yahoo
            ticker_symbol = acao.ticket if acao.ticket.endswith('.SA') else f"{acao.ticket}.SA"
            
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.history(period="7d")
            
            if len(info) >= 2:
                preco_ontem = info['Close'].iloc[-7] # iloc é mais seguro que indice direto
                preco_semana = info['Close'].iloc[-1]
                variacao = ((preco_semana - preco_ontem) / preco_ontem) * 100
                
                # Opcional: Salvar no banco para o Top 10 funcionar depois
                # acao.variacao = variacao
                # acao.save()
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

def buscar_acao(request):
    """
    Captura o texto da pesquisa, limpa espaços e redireciona
    para a página de detalhes.
    """
    query = request.GET.get('q') # Pega o que foi digitado no input name="q"
    
    if query:
        # Garante letra maiúscula e remove espaços extras
        ticket_formatado = query.upper().strip()
        return redirect('detalhes_acao', ticket=ticket_formatado)
    
    return redirect('home')

def home(request):
    # Lógica do Top 10 (baseada no seu código)
    # Filtra, converte variação para número e pega os 10 maiores
    top_10 = (
        Acao.objects
        .filter(variacao__gt=0) # <--- FILTRO NOVO: Somente maior que zero (gt = Greater Than)
        .exclude(variacao__isnull=True)
        .annotate(variacao_num=Cast('variacao', FloatField()))
        .order_by('-variacao_num')[:10]
    )

    context = {
        'template_name': 'home.html', # Mantendo sua lógica original
        'acoes_destaque': top_10
    }
    return render(request, 'index.html', context)

def detalhes_acao(request, ticket):
    # 1. Ajusta o ticket para o padrão do Yahoo (com .SA) e para busca (sem .SA)
    # Garante que está tudo maiúsculo
    ticket_limpo = ticket.upper().replace('.SA', '') 
    symbol = f"{ticket_limpo}.SA" # Ticket para usar na API yfinance

    # 2. Tenta buscar no banco de dados. 
    # Se não achar, cria um objeto "fake" vazio para não dar erro 404.
    acao_banco = Acao.objects.filter(ticket__startswith=ticket_limpo).first()

    # Variáveis iniciais
    info_detalhada = {}
    labels_grafico = []
    dados_grafico = []
    
    # 3. Busca dados na API
    try:
        yf_ticker = yf.Ticker(symbol)
        hist = yf_ticker.history(period="1mo")
        info = yf_ticker.info
        
        # Se a API não retornou histórico, provavelmente o ticket está errado
        if hist.empty:
            return render(request, 'index.html', {
                'template_name': 'home.html', 
                'erro': f'Ação {ticket} não encontrada na Bolsa.'
            })

        # Prepara dados do Gráfico
        for data, linha in hist.iterrows():
            labels_grafico.append(data.strftime('%d/%m'))
            dados_grafico.append(round(linha['Close'], 2))
            
        # Prepara Infos Detalhadas
        info_detalhada = {
            'preco_atual': info.get('currentPrice') or info.get('regularMarketPrice'),
            'max_ano': info.get('fiftyTwoWeekHigh'),
            'min_ano': info.get('fiftyTwoWeekLow'),
            'valor_mercado': info.get('marketCap'),
            'logo_url': info.get('logo_url', ''),
            'dividend_yield': info.get('dividendYield', 0),
            'pl': info.get('trailingPE'),
            'volume_medio': info.get('averageVolume'),
        }

        # 4. TRUQUE: Se não tem no banco, usamos os dados da API para preencher a tela
        if not acao_banco:
            # Criamos um dicionário que imita o objeto Acao
            acao_display = {
                'ticket': symbol,
                'nome_empresa': info.get('longName', ticket), # Pega nome do Yahoo
                'setor': info.get('sector', 'Outros'),        # Pega setor do Yahoo
                'descricao': info.get('longBusinessSummary', 'Descrição não disponível.'),
                'variacao': 0.0
            }
        else:
            # Se tem no banco, usamos os dados de lá (que podem estar traduzidos/editados por você)
            acao_display = acao_banco

    except Exception as e:
        print(f"Erro: {e}")
        return render(request, 'index.html', {
            'template_name': 'home.html', 
            'erro': 'Erro ao conectar com a API.'
        })
    
    ja_favoritou = False
    if request.user.is_authenticated:
        # Verifica se essa ação está na lista do usuário
        ticket_limpo = ticket.upper().replace('.SA', '')
        # Tenta achar no banco pelo ticket limpo ou com .SA
        acao_db = Acao.objects.filter(ticket__startswith=ticket_limpo).first()
        if acao_db:
            ja_favoritou = AcaoFavoritada.objects.filter(usuario=request.user, acao=acao_db).exists()

    context = {
        'acao': acao_display,
        'info_detalhada': info_detalhada,
        'labels_grafico': json.dumps(labels_grafico),
        'dados_grafico': json.dumps(dados_grafico),
        'ja_favoritou': ja_favoritou, # <--- Enviando para o HTML
    }
    return render(request, 'detalhes_acao.html', context)

def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bem-vindo, {user.username}!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'cadastro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Usuário ou senha inválidos.")
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# Perfil (Protegida)
@login_required(login_url='login') # Se não tiver logado, manda pro login
def perfil(request):
    # Passamos os dados do usuário logado (request.user)
    return render(request, 'perfil.html', {'usuario': request.user})

@login_required(login_url='login')
def favoritar_acao(request, ticket):
    ticket_limpo = ticket.upper().replace('.SA', '')
    symbol = f"{ticket_limpo}.SA"
    
    acao_obj, created = Acao.objects.get_or_create(
        ticket=symbol,
        defaults={'nome_empresa': symbol, 'setor': 'Outros'} 
    )
    
    favorito = AcaoFavoritada.objects.filter(usuario=request.user, acao=acao_obj).first()
    
    if favorito:
        favorito.delete()
    else:
        AcaoFavoritada.objects.create(usuario=request.user, acao=acao_obj)
        
    # --- NOVA LÓGICA DE REDIRECIONAMENTO ---
    # Verifica se a URL tem um parâmetro '?next='
    next_page = request.GET.get('next')
    
    if next_page == 'favoritos':
        return redirect('favoritos') # Volta para a lista de favoritos
    
    # Comportamento padrão: vai para detalhes
    return redirect('detalhes_acao', ticket=ticket_limpo)

@login_required(login_url='login')
def favoritos(request):
    # Pega só as ações que o usuário logado favoritou
    favoritas = AcaoFavoritada.objects.filter(usuario=request.user)
    
    acoes_dados = []
    # Monta a lista (pode reutilizar a lógica da lista_rentaveis se quiser buscar cotação atual)
    for item in favoritas:
        acao = item.acao
        # Aqui você pode adicionar a lógica do Yahoo Finance se quiser cotação em tempo real na lista
        acoes_dados.append({
            'ticket': acao.ticket,
            'nome_empresa': acao.nome_empresa,
            'setor': acao.setor,
            'variacao': acao.variacao # Pega a última salva
        })
        
    return render(request, 'favoritos.html', {'acoes': acoes_dados})