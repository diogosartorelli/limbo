import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from assets.funcoes import escreverDados
import json
import pyttsx3
import speech_recognition as sr
import sys

pygame.init()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho) 
pygame.display.set_caption("LIMBO")
icone = pygame.image.load("recursos/icon.jpg")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0, 0)
personagem = pygame.image.load("Recursos/personagem.png")
personagem = pygame.transform.scale(personagem, (110, 110))
fundoStart = pygame.image.load("recursos/fundoStart.png")
fundoJogo = pygame.image.load("recursos/fundoJogo.png")
fundoJogo = pygame.transform.scale(fundoJogo, (1000, 700))
logo = pygame.image.load("recursos/limboLogo.png")
logo = pygame.transform.scale(logo, (320, 120))
fundoDead = pygame.image.load("recursos/fundoDead.png")
fundoDead = pygame.transform.scale(fundoDead, (1000,700))
meteoro = pygame.image.load("recursos/meteoro.png")
meteoro = pygame.transform.scale(meteoro, (220, 260))
missileSound = pygame.mixer.Sound("recursos/meteor_sound.mp3")
explosaoSound = pygame.mixer.Sound("recursos/explosao.mp3")
fonteMenu = pygame.font.SysFont("Papyrus",25)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("recursos/backgroundaudio.mp3")
pygame.mixer.music.play(-1)
nuvem = pygame.image.load ("recursos/nuvem.png")
nuvem = pygame.transform.scale (nuvem , (150, 150))
lua_img_original = pygame.image.load("recursos/lua.png").convert_alpha()



voz = pyttsx3.init()
def falar(mensagem):
    voz.say(mensagem)
    voz.runAndWait()

def ouvir_comando():
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        print("Diga 'iniciar jogo' para começar o jogo...")
        audio = recognizer.listen(mic)
        try:
            comando = recognizer.recognize_google(audio, language='pt-BR')
            return comando.lower()
        except:
            return ""

def tela_boas_vindas(nome_jogador):
    largura_botao = 200
    altura_botao = 50
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                    sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar.collidepoint(evento.pos):
                    return
        
        tela.fill(branco)
        tela.blit(fundoStart, (0, 0))
        
        
        texto_boas_vindas = fonteMenu.render(f"Bem-vindo {nome_jogador}!", True, branco)
        tela.blit(texto_boas_vindas, (400, 200))
        
        
        instrucoes = [
            "Use as setas do teclado para mover o personagem",
            "Desvie dos meteoros que caem do céu",
            "Cada meteoro desviado aumenta sua pontuação",
            "O jogo fica mais difícil conforme você avança!",
            "Clique no botão 'Iniciar jogo' ou apenas diga" ,
            "'iniciar jogo' em voz alta"
        ]
        
        for i, linha in enumerate(instrucoes):
            texto_linha = fonteMenu.render(linha, True, branco)
            tela.blit(texto_linha, (250, 250 + i * 30))
        
        
        botao_iniciar = pygame.draw.rect(tela, branco, 
                                       (400, 470, largura_botao, altura_botao), 
                                       border_radius=20)
        texto_botao = fonteMenu.render("Iniciar Jogo", True, preto)
        tela.blit(texto_botao, (435, 475))
        
        pygame.display.update()
        relogio.tick(60)

        comando_voz = ouvir_comando()
        if "iniciar jogo" in comando_voz:
            return


def jogar():
    largura_janela = 300
    altura_janela = 50
    def obter_nome():
        global nome
        nome = entry_nome.get()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        else:
            root.destroy()

    root = tk.Tk()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", obter_nome)

    entry_nome = tk.Entry(root)
    entry_nome.pack()

    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()

    root.mainloop()
    
    falar(f"Bem-vindo ao Limbo, {nome}!")
    
    tela_boas_vindas(nome)

    posicaoXPersona = 400
    posicaoYPersona = 500
    movimentoXPersona = 0
    movimentoYPersona = 0
    posicaoXMissel = 100
    posicaoYMissel = -240
    velocidadeMissel = 1
    pygame.mixer.music.play(-1)
    pontos = 0
    larguraPersona = 110
    alturaPersona = 110
    larguaMissel = 150
    alturaMissel = 225
    posicaoX_nuvem = random.randint(0, 850)
    posicaoY_nuvem = random.randint(50, 200)
    velocidade_nuvem = random.uniform(0.5, 1.5)
    pausado = False
    raio_lua = 300
    aumentando = True
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                    sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado
                elif evento.key == pygame.K_RIGHT:
                    movimentoXPersona = 15
                elif evento.key == pygame.K_LEFT:
                    movimentoXPersona = -15
            elif evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    movimentoXPersona = 0

        if pausado:
            tela.blit(fundoJogo, (0, 0))
            texto_pause = fonteMorte.render("PAUSE", True, branco)
            tela.blit(texto_pause, (350, 250))
            pygame.display.update()
            continue
                
        posicaoXPersona = posicaoXPersona + movimentoXPersona            
        posicaoYPersona = posicaoYPersona + movimentoYPersona            
        
        if posicaoXPersona < 0:
            posicaoXPersona = 1
        elif posicaoXPersona > 900:
            posicaoXPersona = 899
            
        if posicaoYPersona < 0:
            posicaoYPersona = 15
        elif posicaoYPersona > 473:
            posicaoYPersona = 463
        
        posicaoX_nuvem += velocidade_nuvem
        if posicaoX_nuvem > 1000:
          posicaoX_nuvem = -150  # Reinicia do lado esquerdo
          posicaoY_nuvem = random.randint(50, 200)
          velocidade_nuvem = random.uniform(0.5, 1.5)
        
        if aumentando:
            raio_lua += 0.1
            if raio_lua >= 320:
                aumentando = False
        else:
            raio_lua -= 0.1
            if raio_lua <= 300:
                aumentando = True

        lua_escalada = pygame.transform.smoothscale(lua_img_original, (int(raio_lua), int(raio_lua)))

        tela.fill(branco)
        tela.blit(fundoJogo, (0,0))
        tela.blit(personagem, (posicaoXPersona, posicaoYPersona))
        tela.blit(nuvem, (posicaoX_nuvem, posicaoY_nuvem))
        tela.blit(lua_escalada, (800, -100))


        posicaoYMissel = posicaoYMissel + velocidadeMissel
        if posicaoYMissel > 600:
            posicaoYMissel = -240
            pontos = pontos + 1
            velocidadeMissel = velocidadeMissel + 1
            posicaoXMissel = random.randint(0,800)
            pygame.mixer.Sound.play(missileSound)
            
        tela.blit(meteoro, (posicaoXMissel, posicaoYMissel))
        
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        texto_dica = fonteMenu.render("Press Space to Pause Game", True, branco)

        tela.blit(texto, (15,45))
        tela.blit(texto_dica, (15, 15))
        
        hitbox_width = larguraPersona - 30
        hitbox_height = alturaPersona - 40
        offset_x = 15
        offset_y = 20

        persona_rect = pygame.Rect(posicaoXPersona + offset_x, posicaoYPersona + offset_y, hitbox_width, hitbox_height)
        
        hitbox_width = larguaMissel - 40
        hitbox_height = alturaMissel - 30

        missel_rect = pygame.Rect(posicaoXMissel + 50, posicaoYMissel + 30, hitbox_width, hitbox_height)

        #VER HITBOX
        #pygame.draw.rect(tela, (255, 0, 0), persona_rect, 2)
        #pygame.draw.rect(tela, (0, 0, 255), missel_rect, 2)

        
        if persona_rect.colliderect(missel_rect):
            escreverDados(nome, pontos)
            dead()
        
        pygame.display.update()
        relogio.tick(60)

def start():
    larguraButtonStart = 200
    alturaButtonStart = 55
    larguraButtonQuit = 200
    alturaButtonQuit = 55
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                    sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit = 35
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 150
                    alturaButtonStart = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 150
                    alturaButtonQuit = 40
                    sys.exit()
            
        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        tela.blit(logo, (340, 150))

        startButton = pygame.draw.rect(tela, branco, (400,385, larguraButtonStart, alturaButtonStart), border_radius=20)
        startTexto = fonteMenu.render("Start Game", True, preto)
        tela.blit(startTexto, (430,390))
        
        quitButton = pygame.draw.rect(tela, branco, (400,460, larguraButtonQuit, alturaButtonQuit), border_radius=20)
        quitTexto = fonteMenu.render("Quit Game", True, preto)
        tela.blit(quitTexto, (430,467))
        
        pygame.display.update()
        relogio.tick(60)

def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    larguraButtonStart = 150
    alturaButtonStart = 40
    larguraButtonQuit = 150
    alturaButtonQuit = 40
    

    try:
        with open("log.dat", "r") as f:
            dados = json.load(f)
    except FileNotFoundError:
        dados = {}

    registros = []
    for nome, partidas in dados.items():
        for partida in partidas:
            if len(partidas) == 3:
                pontos, data, hora = partida
                registros.append((nome, pontos, data, hora))

    registros = registros[-5:]  
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit = 35
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 150
                    alturaButtonStart = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 150
                    alturaButtonQuit = 40
                    sys.exit()
                    
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))

        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))

        titulo = fonteMenu.render("Últimas 5 Partidas:", True, branco)
        tela.blit(titulo, (200, 600))

        # Exibir os registros
        for i, (nome, pontos, data, hora) in enumerate(registros):
            texto = fonteMenu.render(f"{i+1}. {nome} | {pontos} pts | {data} {hora}", True, branco)
            tela.blit(texto, (250, 400 + i * 30))

        pygame.display.update()
        relogio.tick(60)

start()