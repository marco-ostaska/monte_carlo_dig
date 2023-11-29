import os
import bancoCentral
import random
import yfinance as yf
import numpy as np
import pandas as pd
from tqdm import tqdm

from datetime import datetime
from tabulate import tabulate


class Carteira:
    ANO_DIAS_UTEIS = 252
    retorno = []
    peso_ativos = []
    volatilidade = []
    volatilidade_ajustada = []
    sharpe_ratio = []
    sortino_ratio = []

    def __init__(self, data, selic):
        self.data = data
        self.numero_ativos = len(data.columns)
        self.selic = selic/100

    def retorno_diario(self):
        return self.data.pct_change().dropna()
    
    def retorno_anual(self):
        return self.retorno_diario().mean() * self.ANO_DIAS_UTEIS


    def cov_anual(self):
        retorno_diario = self.retorno_diario()
        cov_diaria = retorno_diario.cov()
        return cov_diaria * self.ANO_DIAS_UTEIS

    def semi_cov_anual(self):
        retorno_diario = self.retorno_diario()
        rd = retorno_diario[retorno_diario < 0]
        cov_diaria_neg = rd.cov()
        return  cov_diaria_neg * self.ANO_DIAS_UTEIS

    def get_pesos(self, numero_ativos):
        pesos = np.random.random(numero_ativos)
        pesos /= np.sum(pesos)
        return pesos

    def retorno_portfolio(self, pesos):
        return np.dot(pesos, self.retorno_anual())


    def volatilidade_portfolio(self,pesos):
        return np.sqrt(np.dot(pesos.T, np.dot(self.cov_anual(), pesos)))


    def volatilidade_ajustada_portifolio(self, pesos):
        return  np.sqrt(
            np.dot(pesos.T, np.dot(self.semi_cov_anual(), pesos)))

    def calcular_pesos_carteira(self, pesos):
        taxa_livre_risco = self.selic
        retorno_portfolio = self.retorno_portfolio(pesos)
        volatilidade_portfolio = self.volatilidade_portfolio(pesos)
        volatilidade_ajustada = self.volatilidade_ajustada_portifolio(pesos)
        sharpe = (retorno_portfolio - taxa_livre_risco) / \
            volatilidade_portfolio
        sortino = (retorno_portfolio - taxa_livre_risco) / \
            volatilidade_ajustada

        self.retorno.append(retorno_portfolio)
        self.volatilidade.append(volatilidade_portfolio)
        self.volatilidade_ajustada.append(volatilidade_ajustada)

        self.sharpe_ratio.append(sharpe)
        self.sortino_ratio.append(sortino)

        self.peso_ativos.append(pesos)

    def monte_carlo(self, numero_simulacoes):
        #np.random.seed(100)
        for _ in tqdm(range(numero_simulacoes),desc="Criando Carteiras"):
            pesos = self.get_pesos(self.numero_ativos)
            self.calcular_pesos_carteira(pesos)

    def df_carteira(self):

        carteira = {'Retorno': self.retorno,
                    'Risco': self.volatilidade,
                    'Risco Ajustado': self.volatilidade_ajustada,
                    'Sharpe Ratio': self.sharpe_ratio,
                    'Sortino Ratio': self.sortino_ratio}

        for contar,a in enumerate(self.data):
            carteira[a] = [Peso[contar] for Peso in self.peso_ativos]

        # vamos transformar nosso dicionário em um dataframe
        df = pd.DataFrame(carteira)

        # vamos nomear as colunas do novo dataframe
        colunas = ['Retorno', 'Risco', 'Risco Ajustado', 'Sharpe Ratio' , 'Sortino Ratio'] + [a for a in self.data]
        df = df[colunas]

        return df

    def minima_variancia(self):
        df = self.df_carteira()
        valor = df['Risco'].min()
        return df.loc[df['Risco'] == valor]

    def maior_sortino_ratio(self):
        df = self.df_carteira()
        valor = df['Sortino Ratio'].max()
        return df.loc[df['Sortino Ratio'] == valor]

    def maior_sharpe_ratio(self):
        df = self.df_carteira()
        valor = df['Sharpe Ratio'].max()
        return df.loc[df['Sharpe Ratio'] == valor]

    def minima_variancia_ajustada(self):
        df = self.df_carteira()
        valor = df['Risco Ajustado'].min()
        return df.loc[df['Risco Ajustado'] == valor]

    def maior_retorno(self):
        df = self.df_carteira()
        valor = df['Retorno'].max()
        return df.loc[df['Retorno'] == valor]



def format_values(value, is_percentage):
    return f"{value * 100:.2f}%" if is_percentage else f"{value:.2f}"

def format_dataframe(df):
    formatted_df = df.copy()
    for col in formatted_df.columns:
        if "Sharpe Ratio" in col or "Sortino Ratio" in col:
            formatted_df[col] = formatted_df[col].apply(format_values, args=(False,))
        else:
            formatted_df[col] = formatted_df[col].apply(format_values, args=(True,))
    return formatted_df.T   

def print_carteira(df, titulo):
    print()
    print(tabulate(format_dataframe(df), headers=[titulo,"Valores"], tablefmt='simple'))


def get_tickers(tickers):
    #tickers = input("Entre os tickers separados por virgula: ")
    tickers = [t.upper().strip() for t in tickers]
    random.shuffle(tickers)
    return [f"{t}.SA" for t in tickers]

def download_data(tickers, anos_hist):
    hoje = datetime.now()
    start_date=f"{hoje.year-anos_hist}-{datetime.now().month}-{datetime.now().day}"
    data = yf.download(tickers, start=start_date)['Adj Close'].dropna()
    data = data[tickers]  # Reordenando as colunas com base na lista de tickers
    return data

def carteira_to_dict(df, titulo):
    carteira_dict = {
        "Titulo": titulo,
        "Retorno": df["Retorno"].iloc[0] * 100,
        "Risco": df["Risco"].iloc[0] * 100,
        "RiscoAjustado": df["Risco Ajustado"].iloc[0] * 100,
        "Sharpe": df["Sharpe Ratio"].iloc[0],
        "Sortino": df["Sortino Ratio"].iloc[0],
        "Tickers": {ticker: peso * 100 for ticker, peso in zip(df.columns[5:], df.iloc[0][5:].values)}
    }
    return carteira_dict




def process_tickers(tickers, threshold, arquivo, titulo):
    tickers = get_tickers(tickers)
    anos_hist = 5
    data = download_data(tickers, anos_hist)

    print("Tamanho index:", len(data.index), "data:", data)

    if len(data.index) <= 0:
        print ("Erro tentando pegar dados de um ou mais ticker")
        return
    
    taxa_livre_risco = bancoCentral.taxa_livre_risco(anos_hist)

    carteira = Carteira(data, taxa_livre_risco)
    carteira.monte_carlo(10000)
    car = [carteira_to_dict(carteira.maior_sharpe_ratio(), "Maior sharpe ratio"),
        carteira_to_dict(carteira.maior_sortino_ratio(), "Maior sortino ratio")]
    
    for c in car:
        
        print(f"{titulo} | [{c['Titulo']}] | Thr:{threshold} | Retorno:{c['Retorno']} | Sharpe: {c['Sharpe']}| Sortino: {c['Sortino']}")

        if (c["Retorno"] > threshold) and (c["Sharpe"] >= 1) and (c["Sortino"] >= 1):
            # Escrevendo os resultados no arquivo
            with open(f"/tmp/mcd/{arquivo}", 'a') as file:
                file.write(f"{c}\n\n")

def main():

    while True:
            # Lê os tickers de ações da variável de ambiente
        acoes = os.getenv('ACOES_TICKERS', '').split(',')
        acoes_t = float(os.getenv('ACOES_TICKERS_T', 8))
        if acoes and acoes[0]:
            process_tickers(acoes, acoes_t, "acoes.txt", "Ações")

        # Lê os tickers de FII da variável de ambiente
        fii = os.getenv('FII_TICKERS', '').split(',')
        fii_t = float(os.getenv('FII_TICKERS_T', 8))
        if fii and fii[0]:
            process_tickers(fii, fii_t, "fii.txt", "FII")



# Não esqueça de chamar a função main
if __name__ == "__main__":
    main()



if __name__ == "__main__":
    main()




