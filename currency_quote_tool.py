import tkinter as tk
import requests as rq
import pandas as pd
import numpy as np
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter.filedialog import askopenfilename as aof
from datetime import datetime

requisicao = rq.get("https://economia.awesomeapi.com.br/json/all")
dicionario_moedas = requisicao.json()

lista_moedas = list(dicionario_moedas.keys())

def pegarcotacao():
    if combobox_moedas.get() == "":
        label_pedircotacao["text"] = "Nenhuma Moeda Selecionada, Selecione uma Moeda"
        return
    else:
        #tratando o erro de data invalida ou cotacao invalida
        try:
            moeda = combobox_moedas.get()
            data_cotacao = calendario_moeda.get()
            ano = data_cotacao[-4:]
            mes = data_cotacao[3:5]
            dia = data_cotacao[:2]
            link = f"https://economia.awesomeapi.com.br/json/daily/{moeda}-BRL/?start_date={ano}{mes}{dia}&end_date={ano}{mes}{dia}"
            requisicao_moeda = rq.get(link)
            dicionario_moedas1 = requisicao_moeda.json()
            cotacao = dicionario_moedas1[0]["bid"]
            cotacao = float(cotacao)
            cotacao = f"A Cotação da Moeda {moeda} no dia {dia}/{mes}/{ano} é de R${cotacao:,.2f}"
            label_pedircotacao["text"] = cotacao
            return
        except:
            label_pedircotacao["text"] = "Erro ao Pegar a Cotação, Verifique se a Moeda e a Data estão Corretas"
            return

def selecionar_arquivo():
    caminho_arquivo = aof(title='Selecione um arquivo em Excel para abrir', filetypes=[('Excel', '*.xlsx')])
    var_caminho_arquivo.set(caminho_arquivo)
    if caminho_arquivo:
        label_pedircotacaomultiplasmoedas["text"] = f"Arquivo Selecionado: {caminho_arquivo}"

def atualizar_cotacoes():
    # try:
        # ler o dataframe de moedas
        df = pd.read_excel(var_caminho_arquivo.get())
        print(df)
        moedas = df.iloc[:, 0]
        # pegar a data de inicio e fim das cotacoes
        data_inicial = datainicial.get()
        data_final = datafinal.get()
        ano_inicial = data_inicial[-4:]
        mes_inicial = data_inicial[3:5]
        dia_inicial = data_inicial[:2]

        ano_final = data_final[-4:]
        mes_final = data_final[3:5]
        dia_final = data_final[:2]


        # para cada moeda
        for moeda in moedas:
            # pegar todas as cotações daquela moeda
            link = f"https://economia.awesomeapi.com.br/json/daily/{moeda}-BRL/?start_date={ano_inicial}{mes_inicial}{dia_inicial}&end_date={ano_final}{mes_final}{dia_final}"
            requisicao_moeda = rq.get(link)
            cotacoes = requisicao_moeda.json()
            for cotacao in cotacoes:
                timestamp = int(cotacao["timestamp"])
                bid = float(cotacao["bid"])
                data = datetime.fromtimestamp(timestamp)
                data = data.strftime("%d/%m/%Y")
                if data not in df:
                    df[data] = np.nan
                # criar uma coluna em um novo dataframe com as cotacoes
                df.loc[df.iloc[:, 0] == moeda, data] = bid
        # criar um arquivo com todas as cotacoes
        df.to_excel("Cotações Atualizadas.xlsx")
        label_atualizarcotacoes["text"] = "Cotações Atualizadas com Sucesso"        
            
    # except:
    #     label_atualizarcotacoes["text"] = "Selecione um Arquivo em Excel para Atualizar as Cotações de formato correto"
    #     return


janela = tk.Tk()

janela.title("Ferramenta de Cotação de Moedas")

label_cotacaomoeda = tk.Label(janela, text="Cotação de uma Moeda Especifica", borderwidth=2, relief="solid", font=("Arial", 12), anchor="center")
label_cotacaomoeda.grid(column=0, row=0, padx=10, pady=10, sticky="NSEW", columnspan=3)

label_selecionarmoeda = tk.Label(janela, font=("Arial", 11), text="Selecione a Moeda", anchor="center")
label_selecionarmoeda.grid(column=0, row=1, padx=10, pady=10, sticky="NSEW", columnspan=2)

combobox_moedas = ttk.Combobox(values=lista_moedas, font=("Arial", 10), width=10)
combobox_moedas.grid(column=2, row=1, padx=10, pady=10, sticky="NSEW")

label_selecionardiadepegarcotaca = tk.Label(janela, font=("Arial", 11), text="Selecione o dia que deseja pegar a cotação", anchor="center")
label_selecionardiadepegarcotaca.grid(column=0, row=2, padx=10, pady=10, sticky="NSEW", columnspan=2)

calendario_moeda = DateEntry(year=2023, locate='pt_br')
calendario_moeda.grid(column=2, row=2, padx=10, pady=10, sticky="NSEW")

label_pedircotacao = tk.Label(janela, font=("Arial", 11), text="", anchor="w")
label_pedircotacao.grid(column=0, row=3, padx=10, pady=10, sticky="NSEW", columnspan=2)

botao_pedircotacao = tk.Button(janela, text="Pegar Cotação", font=("Arial", 10), anchor="center", command=pegarcotacao)
botao_pedircotacao.grid(column=2, row=3, padx=10, pady=10, sticky="NSEW")

# cotacao de varias moedas
label_cotacaovariasmoedas = tk.Label(janela, text="Cotação de Multiplas Moedas", borderwidth=2, relief="solid", font=("Arial", 12), anchor="center")
label_cotacaovariasmoedas.grid(column=0, row=4, padx=10, pady=10, sticky="NSEW", columnspan=3)

label_selecionararquivo = tk.Label(janela, font=("Arial", 11), text="Selecione um arquivo em Excel com as moedas na Coluna A", anchor="center")
label_selecionararquivo.grid(column=0, row=5, padx=10, pady=10, sticky="NSEW", columnspan=2)

var_caminho_arquivo = tk.StringVar()

botao_selecionararquivo = tk.Button(janela, text="Clique para Selecionar o Arquivo", font=("Arial", 10), anchor="center", command=selecionar_arquivo)
botao_selecionararquivo.grid(column=2, row=5, padx=10, pady=10, sticky="NSEW")

label_pedircotacaomultiplasmoedas = tk.Label(janela, font=("Arial", 11), text="Nenhum Arquivo Selecionado", anchor="e")
label_pedircotacaomultiplasmoedas.grid(column=0, row=6, padx=10, pady=10, sticky="NSEW", columnspan=3)

# cotacao de acordo com as datas inicial e final
label_diainicial = tk.Label(janela, font=("Arial", 11), text="Data Inicial", anchor="e")
label_diainicial.grid(column=0, row=7, padx=10, pady=10, sticky="NSEW")

datainicial = DateEntry(year=2023, locate='pt_br')
datainicial.grid(column=1, row=7, padx=10, pady=10, sticky="NSEW")

label_diafinal = tk.Label(janela, font=("Arial", 11), text="Data Final", anchor="e")
label_diafinal.grid(column=0, row=8, padx=10, pady=10, sticky="NSEW")

datafinal = DateEntry(year=2023, locate='pt_br')
datafinal.grid(column=1, row=8, padx=10, pady=10, sticky="NSEW")

botao_atualizarcotacoes = tk.Button(janela, text="Atualizar Cotações", font=("Arial", 10), anchor="center", command=atualizar_cotacoes)
botao_atualizarcotacoes.grid(column=0, row=9, padx=10, pady=10, sticky="NSEW")

label_atualizarcotacoes = tk.Label(janela, font=("Arial", 11), text="", anchor="e")
label_atualizarcotacoes.grid(column=1, row=9, padx=10, pady=10, sticky="NSEW", columnspan=2)

botao_fechar = tk.Button(janela, text="Fechar", font=("Arial", 10), anchor="center", command=janela.quit)
botao_fechar.grid(column=2, row=10, padx=10, pady=10, sticky="NSEW")

janela.mainloop()