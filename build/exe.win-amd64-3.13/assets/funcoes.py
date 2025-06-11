import os, time
import json
from datetime import datetime


def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
    
def escreverDados(nome, pontos):
    arquivo = "log.dat"
    dados = {}

    # Carrega os dados existentes (se houver)
    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                dados = {}

    # Obtém data e hora atual
    agora = datetime.now()
    data = agora.strftime("%d/%m/%Y")
    hora = agora.strftime("%H:%M:%S")

    # Cria a lista de partidas se ainda não existir
    if nome not in dados:
        dados[nome] = []

    # Adiciona o novo registro (pontuação, data, hora)
    dados[nome].append([pontos, data, hora])

    # Salva de volta no arquivo
    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)
    
    # END - inserindo no arquivo