import pygame
import time
import math

# Define as dimensões da tela
screen_width = 600
screen_height = 400

# Inicializa o Pygame
pygame.init()
# Cria a janela do jogo
window = pygame.display.set_mode((screen_width, screen_height))
# Define a fonte para exibir a pontuação
font = pygame.font.SysFont('Tohama', 40, True, False)

# Classe para representar os jogadores


class Player():
    def __init__(self, x, y, a, b, c):
        self.x = x  # Posição X do jogador
        self.y = y  # Posição Y do jogador
        self.w = 20  # Largura da raquete
        self.h = 100  # Altura da raquete
        self.__init__speed = 10  # Velocidade inicial de movimento da raquete
        self.speed = 10  # Velocidade de movimento da raquete
        self.points = 0  # Pontuação do jogador
        self.cor = (a, b, c)  # Cor da raquete

        self.up = False  # Flag para mover a raquete para cima
        self.down = False  # Flag para mover a raquete para baixo
        self.time = True  # Flag de tempo (não utilizada no código)

    def revert(self):
        self.speed = self.__init__speed

    def velo(self):
        self.speed *= 1.1

    def reset(self):
        self.speed = self.__init__speed

    # Define a flag para mover a raquete para cima
    def setUp(self, mode):
        self.up = mode

    # Define a flag para mover a raquete para baixo
    def setDown(self, mode):
        self.down = mode

    # Define a flag de tempo (não utilizada no código)
    def setTime(self, mode):
        self.time = mode

    # Atualiza a posição da raquete
    def update(self):
        if (self.up):
            if (self.y > 0):
                self.y -= self.speed
            else:
                self.y = 0
        elif (self.down):
            if (self.y < screen_height - self.h):
                self.y += self.speed
            else:
                self.y = screen_height - self.h

    # Renderiza a raquete na tela
    def render(self, window):
        pygame.draw.rect(window, self.cor, pygame.Rect(
            self.x, self.y, self.w, self.h))

# Classe para representar a bola


class Ball():
    def __init__(self, x, y, dy, a, b, c):
        self.x = x  # Posição X da bola
        self.y = y  # Posição Y da bola
        self.init_x = x  # Posição inicial X da bola
        self.init_y = y  # Posição inicial Y da bola
        self.init_dy = dy  # Velocidade inicial Y da bola
        self.init_dx = -10  # Velocidade inicial X da bola
        self.r = 30  # Raio da bola
        self.dx = -10  # Velocidade de movimento X da bola
        self.dy = dy  # Velocidade de movimento Y da bola
        self.cor = (a, b, c)  # Cor da bola

    def vel(self):
        self.dx *= 1.1

    # Inverte a direção X da bola e aumenta a velocidade
    def revertX(self):
        self.dx *= -1
        self.init_dx *= -1

    # Reseta a posição da bola para a posição inicial

    def reset(self):
        self.revertX()
        self.x = self.init_x
        self.y = self.init_y
        self.dx = self.init_dx
        self.dy = self.init_dy

    # Atualiza a posição da bola
    def update(self):
        if (self.y + self.r) >= screen_height or (self.y) <= 0:
            self.dy *= -1
        self.x += self.dx
        self.y += self.dy

    # Renderiza a bola na tela
    def render(self, window):
        pygame.draw.ellipse(window, self.cor, pygame.Rect(
            self.x, self.y, self.r, self.r))


# Variáveis dos jogadores e da bola
player_1 = Player(screen_width-30, 120, 255, 0, 0)
player_2 = Player(10, 120, 0, 0, 255)
ball = Ball(screen_width // 2, screen_height // 2, 5, 255, 255, 255)

running = True

# Loop principal do jogo
while (running):
    # Preenche a tela com uma cor de fundo
    pygame.draw.rect(window, (0, 200, 100), pygame.Rect(
        0, 0, screen_width, screen_height))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Verifica se uma tecla foi pressionada
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_1.setUp(True)
            if event.key == pygame.K_DOWN:
                player_1.setDown(True)
            if event.key == pygame.K_w:
                player_2.setUp(True)
            if event.key == pygame.K_s:
                player_2.setDown(True)
        # Verifica se uma tecla foi solta
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_1.setUp(False)
            if event.key == pygame.K_DOWN:
                player_1.setDown(False)
            if event.key == pygame.K_w:
                player_2.setUp(False)
            if event.key == pygame.K_s:
                player_2.setDown(False)

    # Atualiza a posição dos jogadores e da bola
    player_1.update()
    player_2.update()
    ball.update()

    # Cria retângulos para detectar colisões
    ball_rect = pygame.Rect(ball.x - 10, ball.y, ball.r + 10, ball.r + 10)
    player1_rect = pygame.Rect(player_1.x, player_1.y, player_1.w, player_1.h)
    player2_rect = pygame.Rect(player_2.x, player_2.y, player_2.w, player_2.h)

    # Verifica colisão da bola com as raquetes

    if (ball_rect.colliderect(player1_rect)):
        ball.revertX()
        ball.vel()
        Player.velo(player_1)

    if (ball_rect.colliderect(player2_rect)):
        ball.revertX()
        ball.vel()
        Player.velo(player_2)

    # Verifica se a bola saiu pela esquerda
    if (ball.x < 10):
        ball.reset()
        Player.revert(player_1)
        Player.revert(player_2)
        player_2.points += 1

    # Verifica se a bola saiu pela direita
    if (ball.x > screen_width - 20):
        ball.reset()
        Player.revert(player_1)
        Player.revert(player_2)
        player_1.points += 1

    # Renderiza a pontuação dos jogadores
    pontos_p1 = font.render(str(player_1.points), False, (255, 255, 255))
    window.blit(pontos_p1, (10, 20))
    pontos_p2 = font.render(str(player_2.points), False, (255, 255, 255))
    window.blit(pontos_p2, (screen_width - 30, 20))

    # Renderiza os jogadores e a bola na tela
    player_1.render(window)
    player_2.render(window)
    ball.render(window)

    # Atualiza a tela
    pygame.display.update()
    # Define a taxa de atualização
    time.sleep(0.03)
