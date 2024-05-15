import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Definição de constantes
WIDTH, HEIGHT = 400, 600
GRAVITY = 0.25
FLAP_FORCE = -5
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuração da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Carregamento de recursos
try:
    bird_img = pygame.image.load_extended("bird.png").convert_alpha()
except pygame.error as e:
    print("Erro ao carregar a imagem:", e)
    pygame.quit()
    sys.exit()
bird_img = pygame.transform.scale(bird_img, (40, 40))

pipe_img = pygame.Surface((50, HEIGHT))
pipe_img.fill((0, 255, 0))

# Carregar imagem de fundo
background_img = pygame.image.load("background.png").convert()

# Posição inicial do fundo
background_x = 0

# Velocidade de deslocamento do fundo
background_speed = 1

# Classe para o pássaro
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = bird_img
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(100, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Rotação do pássaro
        if self.velocity < 0:  # Pássaro subindo
            self.image = pygame.transform.rotate(self.original_image, 20)
        else:  # Pássaro caindo
            self.image = pygame.transform.rotate(self.original_image, -20)

# Classe para os obstáculos (tubos)
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pipe_img
        self.rect = self.image.get_rect(midtop=(x, HEIGHT // 2))
        self.speed = 3
        self.direction = random.choice([-1, 1])  # Define a direção inicial

    def update(self):
        self.rect.x -= self.speed
        self.rect.y += self.direction  # Move o tubo para cima ou para baixo

        # Inverte a direção quando atinge os limites superior ou inferior
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.direction *= -1

# Função para gerar um par de obstáculos (tubos)
def create_pipe():
    gap_y = random.randint(150, HEIGHT - 300)
    bottom_pipe = Pipe(WIDTH + 50)
    top_pipe = Pipe(WIDTH + 50)
    bottom_pipe.rect.bottom = gap_y - 100
    top_pipe.rect.top = gap_y + 100
    pipes.add(bottom_pipe)
    pipes.add(top_pipe)
    all_sprites.add(bottom_pipe)
    all_sprites.add(top_pipe)

# Inicialização das sprites
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()
bird = Bird()
all_sprites.add(bird)

# Contador de frames para geração de obstáculos
frame_count = 0

# Loop principal do jogo
running = True
while running:
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.velocity = FLAP_FORCE  # Apenas definindo a velocidade diretamente para o flap

    # Atualização
    all_sprites.update()

    # Verificar colisões entre o pássaro e os obstáculos
    hits = pygame.sprite.spritecollide(bird, pipes, False)
    if hits or bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT:
        running = False

    # Geração de obstáculos a cada 100 frames
    frame_count += 1
    if frame_count == 100:
        create_pipe()
        frame_count = 0

    # Atualização da posição do fundo
    background_x -= background_speed

    # Se o fundo sair completamente da tela, reinicie sua posição
    if background_x <= -WIDTH:
        background_x = 0

    # Renderização
    screen.blit(background_img, (background_x, 0))  # Desenha o fundo na tela
    all_sprites.draw(screen)  # Desenhe outros elementos do jogo (pássaro, obstáculos, etc.)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()
