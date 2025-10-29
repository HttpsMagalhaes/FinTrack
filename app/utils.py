import yfinance as yf
import pandas as pd

def get_stock_data(symbol, period='1mo', interval='1d'):
    """
    Função para buscar dados históricos de ações usando a API do Yahoo Finance.
    :param symbol: código da ação (ex: 'PETR4.SA')
    :param period: período (ex: '1mo', '3mo', '1y')
    :param interval: intervalo (ex: '1d', '1wk', '1h')
    :return: DataFrame com as informações da ação ou None se não houver dados
    """
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        if df.empty:
            print("Nenhum dado encontrado para o símbolo:", symbol)
            return None
        df = df.reset_index()
        df.columns = [col.lower() for col in df.columns]  # padronizar nomes
        return df
    except Exception as e:
        print("Erro no yfinance:", e)
        return None
