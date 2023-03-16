import os
import random
import pygame
from pygame.locals import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()

#Tela
largura, altura = 600, 680
tela = pygame.display.set_mode((largura, altura)) #Cria uma superfície principal ou surface
pygame.display.set_caption('')
branco = corR, corG, corB = 255, 255, 255
preto = corR, corG, corB = 0, 0, 0
Clock = pygame.time.Clock()
running = True #Variavel de controle do loop

#Fundo do Game e musica tema
fundo = pygame.transform.scale(pygame.image.load(os.path.join('assets/fundo', 'fundo.png')).convert_alpha(), (largura, altura))
pygame.mixer.music.set_volume(1) #Setando voluno de musica de fundo
musica_tema = pygame.mixer.music.load(os.path.join('assets/sounds', 'tema.wav'))
pygame.mixer.music.play(-1)

#Efeitos sonoros
sound_plasma = pygame.mixer.Sound(os.path.join('assets/sounds', 'plasma.wav'))
sound_explosion =  pygame.mixer.Sound(os.path.join('assets/sounds', 'explosion.wav'))
sound_explosion2 =  pygame.mixer.Sound(os.path.join('assets/sounds', 'explosion02.wav'))
sound_impact_plasma = pygame.mixer.Sound(os.path.join('assets/sounds', 'plasma_impact.wav'))



#fonte
fonte = pygame.font.Font(os.path.join('assets/fonts', 'font.ttf'), 15)
fonte2 = pygame.font.Font(os.path.join('assets/fonts', 'font.ttf'), 30)

#Inimigos
alien_X = 550
alien_Y = 0
alien_ship1 = pygame.transform.scale(pygame.image.load(os.path.join('assets/ships', 'ini_1.png')).convert_alpha(), (50, 50))
alien_ship2 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('assets/ships', 'ini_2.png')).convert_alpha(), (50, 50)), -180)
alien_ship3 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('assets/ships', 'ini_3.png')).convert_alpha(), (50, 50)), -180)
alien_ship4 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('assets/ships', 'ini_4.png')).convert_alpha(), (50, 50)), -180)

#Escolher de alien
tipos_aliens = [alien_ship1, alien_ship2, alien_ship3, alien_ship4]
alien = random.choice(tipos_aliens)

#DeathShip
pos_jogadorX = 280 
pos_joagadorY = 550   
deathship = pygame.transform.scale(pygame.image.load(os.path.join('assets/ships', 'deathship.png')).convert_alpha(), (50, 50))

#Plasma Player
plasma_shot = pygame.transform.scale(pygame.image.load(os.path.join('assets/ships', 'shot_ds.png')).convert_alpha(), (20, 30))
vel_y_plasma = 0
plasma_pronto = True
pos_plasma_shotX = 295
pos_plasma_shotY = 550
gatilho = False

#Rects
deathship_rect = deathship.get_rect()
plasma_rect = plasma_shot.get_rect()
alien_rect = alien.get_rect()

#Pontução
saude = 100
record = 0
pontos = 0
record_db = 'assets/db/record.txt'


#Funções
def colisao():
    global pontos
    global saude
    if deathship_rect.colliderect(alien_rect):
        pontos -= 2
        saude -= 5
        return True
    elif alien_rect.y >= 600:
        pontos -= 4
        return True
    elif plasma_rect.colliderect(alien_rect):
        pontos += 1
        return True
    else:
        return False

def colisao_sound():
    if deathship_rect.colliderect(alien_rect):
        saida = random.choice([sound_explosion, sound_explosion2])
        return saida.play()
    elif plasma_rect.colliderect(alien_rect):
        
        return sound_impact_plasma.play()


def respawn_alien():
    alien = random.choice(tipos_aliens)
    x = random.randint(1, 545)
    y = 0
    return [alien, x, y]


def respawn_plasma():
    gatilho = False
    plasma_pronto = True
    respawn_plasmaX, respawn_plasmaY = pos_jogadorX + 15, pos_joagadorY
    vel_y_plasma = 0
    return [plasma_pronto, respawn_plasmaX, respawn_plasmaY, gatilho, vel_y_plasma]

while running:
    Clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Fundo Dinâmico
    rel_altura = altura % fundo.get_rect().height
    tela.blit(fundo, (0, rel_altura - fundo.get_rect().height))
    if rel_altura < 1280:
        tela.blit(fundo, (0, rel_altura))
    altura += 3
  
    #Pos rects
    deathship_rect.x = pos_jogadorX
    deathship_rect.y = pos_joagadorY
    plasma_rect.x = pos_plasma_shotX
    plasma_rect.y = pos_plasma_shotY
    alien_rect.x = alien_X
    alien_rect.y = alien_Y

    
    #Salva Pontuação
    if os.path.isfile(record_db):
            with open(record_db,  'r+') as gravacao:
                if int(gravacao.read()) < pontos:
                    with open(record_db, 'w+') as gravacao:
                        gravacao.write(str(pontos))
    else:
        with open(record_db, 'w+') as gravacao:
            gravacao.write(str(pontos))

    #Satus
    with open(record_db, 'r+') as gravacao:
        rec_numero = int(gravacao.read())
    show_record = fonte.render(f'Record: {int(rec_numero)}', True, (128,128,128))
    tela.blit(show_record, (10, 645))
    score = fonte.render(f'Pontos: {int(pontos)}', True, (255, 255, 255))
    tela.blit(score, (10, 660))
    hp = fonte.render(f'Vida: {int(saude)}', True, (255, 255, 255))
    tela.blit(hp, (530, 660))

    #Controles do Player e movimentos
    comando = pygame.key.get_pressed()
    if comando[pygame.K_a] and pos_jogadorX > 1 or comando[pygame.K_LEFT] and pos_jogadorX > 1:
        pos_jogadorX -= 6
        if not gatilho:
            pos_plasma_shotX -= 6
    if comando[pygame.K_d] and pos_jogadorX < 545 or comando[pygame.K_RIGHT] and pos_jogadorX < 545:
        pos_jogadorX += 6
        if not gatilho:
            pos_plasma_shotX += 6

    if comando[pygame.K_SPACE] and plasma_pronto == True: #Quando ESPAÇO for precionando, o plasma é acionando 
        gatilho = True
        plasma_pronto = False
        vel_y_plasma = 10
        sound_plasma.play() 
 
    if ((pos_joagadorY - pos_plasma_shotY) >= 600) and plasma_pronto == False:
        plasma_pronto, pos_plasma_shotX, pos_plasma_shotY, gatilho, vel_y_plasma = respawn_plasma()

    if alien_Y == 630 or colisao():
        alien, alien_X, alien_Y = respawn_alien()

    pos_plasma_shotY -= vel_y_plasma

    if pontos < 100:
        alien_Y += 4
    elif pontos >= 100:
        alien_Y += 6
    elif pontos >= 200:
        alien += 8

    if pontos < 0 or saude < 0:
        running = False

    colisao_sound()
    tela.blit(alien, (alien_X, alien_Y))
    tela.blit(plasma_shot, (pos_plasma_shotX, pos_plasma_shotY))
    tela.blit(deathship, (pos_jogadorX, pos_joagadorY))

   
    pygame.display.update()

# Desenvolvido por: Erik (20211P2TIXXXX)
# Obs: Somente por mim!!!!!   /,,/, ( x_x) /,,/,