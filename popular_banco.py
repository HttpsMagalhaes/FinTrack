import os
import django
import yfinance as yf

# Configura o Django (ajuste para o nome do seu projeto)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from app.models import Acao

# Lista de alguns dos principais tickers da B3
tickers = [
    "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "ABEV3.SA", "BBAS3.SA", "WEGE3.SA",
    "JBSS3.SA", "GGBR4.SA", "EQTL3.SA", "LREN3.SA", "RADL3.SA", "NTCO3.SA", "RENT3.SA",
    "HAPV3.SA", "RAIL3.SA", "SUZB3.SA", "PRIO3.SA", "VIVT3.SA", "BRFS3.SA", "ELET3.SA",
    "CMIG4.SA", "CSNA3.SA", "KLBN11.SA", "EGIE3.SA", "B3SA3.SA", "ENEV3.SA", "CYRE3.SA",
    "MRVE3.SA", "USIM5.SA"
]

print("Atualizando banco de dados com ações válidas...")

for ticker in tickers:
    try:
        dados = yf.Ticker(ticker)
        info = dados.info

        nome = info.get('longName', 'Desconhecido')
        setor = info.get('sector', 'Não informado')
        descricao = info.get('longBusinessSummary', 'Sem descrição disponível')
        variacao = info.get('regularMarketChangePercent')


        # 🔹 Limpeza robusta de caracteres e tipos
        if isinstance(variacao, str):
            variacao = variacao.strip().replace('—', '').replace('%', '').replace(',', '.')
            if not variacao or not any(c.isdigit() for c in variacao):
                variacao = 0.0

        try:
            variacao = float(variacao)
        except (ValueError, TypeError):
            variacao = 0.0

        # Ignora ações que não têm nome ou setor válido
        if nome == 'Desconhecido' or setor == 'Não informado':
            print(f"Ignorando {ticker}: informações insuficientes.")
            continue

        # Cria ou atualiza o registro
        Acao.objects.update_or_create(
            ticket=ticker,
            defaults={
                'nome_empresa': nome,
                'setor': setor,
                'descricao': descricao,
                'variacao': variacao,
            }
        )

        print(f"{ticker} atualizado com sucesso!")

    except Exception as e:
        print(f"Erro ao processar {ticker}: {e}")

print("Finalizado!")
