import pygame
from pygame.locals import (
    KEYDOWN,
    QUIT,
)

from game import Game
from player import Player
from enemy import Enemy
from cloud import Cloud


# Definir constantes para a largura e altura da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Configuração para sons, os padrões são bons
pygame.mixer.init()
game_over_music = pygame.mixer.Sound("musics/smgameover.mp3")


# Inicializa o pygame
pygame.init()

# Configure o relógio para uma taxa de quadros decente
clock = pygame.time.Clock()

# Cria o objeto de tela
# O tamanho é determinado pelas constantes SCREEN_WIDTH e SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Crie eventos personalizados para adicionar um novo inimigo e nuvem
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Crie nosso 'jogador'
player = Player()

# Armazena a posição inicial do jogador
initial_player_position = player.rect.topleft


# Crie grupos para conter sprites inimigos, sprites de nuvem e todos os sprites
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# Carregue e reproduza nossa música de fundo
pygame.mixer.music.load("musics/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Carregue todos os nossos arquivos de som
collision_sound = pygame.mixer.Sound("musics/Collision.ogg")

# Defina o volume base para todos os sons
collision_sound.set_volume(0.5)

# Variável para manter nosso loop principal rodando
running = True

# Cria uma instância do jogo
game = Game()

# Carregue a imagem para a tela de título
title_image = pygame.image.load("src/peakpx.jpg")

# Game initialization loop
game_start = False
while not game_start:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == pygame.K_SPACE:  # Verifica se a tecla pressionada é a barra de espaço
            game_start = True
        elif event.type == QUIT:
            running = False
            game_start = True

    # Mostra a tela de título
    screen.fill((0, 0, 0))
    screen.blit(title_image, (0, 0))
    title_font = pygame.font.Font(None, 36)
    title_text = title_font.render("Press SPACE to start", True, (255, 255, 255))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    clock.tick(30)

# Variável para acompanhar a pontuação
score = 0

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)



    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)

    enemies.update()
    clouds.update()

    # Preencha a tela com preto
    screen.fill((135, 206, 250))

    # Desenha todos os sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

        # Aumente a pontuação com base no tempo decorrido
        score += clock.get_time() / 1000

    if pygame.sprite.spritecollideany(player, enemies):
        player.rect.topleft = initial_player_position
        collision_sound.play()
        game.reduce_life()

    if game.is_game_over():
        pygame.mixer.music.stop()
        game_over_music.play()

        screen.fill((0, 0, 0))
        game_over_font = pygame.font.Font(None, 36)
        game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.mixer.music.stop()  # Para a música de fundo atual, se estiver tocando
        game_over_music.play()  # Reproduz a música de game over

        # Renderiza a pontuação na tela de game over
        score_font = pygame.font.Font(None, 30)
        score_text = score_font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

        pygame.display.flip()
        # Loop para aguardar o jogador fechar a janela
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False  # Sai do loop e encerra o jogo

    # Desenhe a pontuação e a vida na tela
    score_font = pygame.font.Font(None, 30)
    score_text = score_font.render("Score: {:.2f}".format(score), True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))

    life_text = score_font.render("Life: " + str(game.get_life()), True, (255, 255, 255))
    screen.blit(life_text, (SCREEN_WIDTH - life_text.get_width() - 10, 10))

    # Atualize a pontuação quando os inimigos são evitados
    if player.rect.top <= 0:
        player.rect.topleft = initial_player_position
        game.increase_score(10)

    pygame.display.flip()
    clock.tick(30)

# Clean up
pygame.quit()
