import os
import django
import yfinance as yf

# Configura o Django (ajuste para o nome do seu projeto)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from app.models import Acao

tickers = [
    'PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA',
    'BBAS3.SA', 'WEGE3.SA', 'MGLU3.SA', 'RENT3.SA', 'SUZB3.SA',
    'ELET3.SA', 'ELET6.SA', 'RAIL3.SA', 'CMIG4.SA', 'GGBR4.SA',
    'CSNA3.SA', 'KLBN11.SA', 'PRIO3.SA', 'BRFS3.SA', 'JBSS3.SA',
    'EQTL3.SA', 'HAPV3.SA', 'LREN3.SA', 'B3SA3.SA', 'CYRE3.SA',
    'CCRO3.SA', 'CPLE6.SA', 'ENBR3.SA', 'EGIE3.SA', 'TOTS3.SA'
]

for ticker in tickers:
    try:
        dados = yf.Ticker(ticker).info

        nome_empresa = dados.get('longName', 'Desconhecido')
        setor = dados.get('sector', 'Não informado')
        descricao = dados.get('longBusinessSummary', 'Sem descrição disponível.')

        Acao.objects.update_or_create(
            ticket=ticker,
            defaults={
                'nome_empresa': nome_empresa,
                'setor': setor,
                'descricao': descricao
            }
        )

        print(f"{ticker} - {nome_empresa} adicionada/atualizada.")

    except Exception as e:
        print(f"Erro ao adicionar {ticker}: {e}")

print("População do banco concluída!")
