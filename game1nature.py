import pygame
from sys import exit
import random
import os

# directory de base pour les assets
DOSSIER_BASE = os.path.dirname(__file__)

# Game Constants
GAME_WIDTH = 360
GAME_HEIGHT = 640
BIRD_X = GAME_WIDTH / 8
BIRD_Y = GAME_HEIGHT / 2
BIRD_WIDTH, BIRD_HEIGHT = 34, 24
PIPE_WIDTH, PIPE_HEIGHT = 64, 512

class Bird(pygame.Rect):
    def __init__(self, img):
        super().__init__(BIRD_X, BIRD_Y, BIRD_WIDTH, BIRD_HEIGHT)
        self.img = img

class Pipe(pygame.Rect):
    def __init__(self, img, x, y):
        super().__init__(x, y, PIPE_WIDTH, PIPE_HEIGHT)
        self.img = img
        self.passed = False

# Initialization de pygame
pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
clock = pygame.time.Clock()
text_font = pygame.font.SysFont("Comic Sans MS", 45)

#load images
def load_img(name, size=None):
    path = os.path.join(DOSSIER_BASE, "image", name)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size) if size else img

try:
    background_image = load_img("flappybirdbg.png", (GAME_WIDTH, GAME_HEIGHT))
    bird_image = load_img("flappybird.png", (BIRD_WIDTH, BIRD_HEIGHT))
    top_pipe_img = load_img("toppipe.png", (PIPE_WIDTH, PIPE_HEIGHT))
    bottom_pipe_img = load_img("bottompipe.png", (PIPE_WIDTH, PIPE_HEIGHT))
except pygame.error as e:
    print(f"Error loading images: {e}. Check your file extensions!")
    # placeholder si images fail
    background_image = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    bird_image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
    top_pipe_img = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT))
    bottom_pipe_img = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT))

# Game State
bird = Bird(bird_image)
pipes = []
velocity_y = 0
gravity = 0.25  # graviter faible pour meilleur experience
score = 0
game_over = False

def reset_game():
    global score, game_over, velocity_y, pipes
    bird.y = BIRD_Y
    velocity_y = 0
    pipes.clear()
    score = 0
    game_over = False

def create_pipes():
    gap = 150
    random_y = random.randint(100, GAME_HEIGHT - gap - 100)
    # Top pipe
    pipes.append(Pipe(top_pipe_img, GAME_WIDTH, random_y - PIPE_HEIGHT))
    # Bottom pipe
    pipes.append(Pipe(bottom_pipe_img, GAME_WIDTH, random_y + gap))

# Timer
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

victory_time = 0
victory_achieved = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == SPAWNPIPE and not game_over and not victory_achieved:
            create_pipes()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP):
                if game_over:
                    reset_game()
                elif not victory_achieved:
                    velocity_y = -6

        if score >= 10:
                    victory_achieved = True
                    victory_start_time = pygame.time.get_ticks() # Start the 5s timer
                    pygame.quit()
                    exit()
    if not game_over:
        # Bird Physics
        velocity_y += gravity
        bird.y += velocity_y
        
        # collision floor/roof
        if bird.bottom >= GAME_HEIGHT or bird.top <= 0:
            game_over = True

        # Pipe logic
        for pipe in pipes[:]:
            pipe.x -= 3
            if bird.colliderect(pipe):
                game_over = True
            if not pipe.passed and bird.left > pipe.right:
                score += 0.5 
                pipe.passed = True
            if pipe.right < 0:
                pipes.remove(pipe)

    # Drawing
    window.blit(background_image, (0, 0))
    for pipe in pipes:
        window.blit(pipe.img, pipe)
    window.blit(bird.img, bird)


    # UI
    score_surface = text_font.render(f"{int(score)}", True, (255, 255, 255))
    window.blit(score_surface, (GAME_WIDTH//2 - 10, 50))
    
    if victory_achieved:
        # texte de victoire
        victory_font = pygame.font.SysFont("Comic Sans MS", 50)
        win_text = victory_font.render("Tu as gagné(e)", True, (255, 0, 0))
        window.blit(win_text, (GAME_WIDTH//2 - 100, GAME_HEIGHT//2))
        
        # Check si 5 sec sont passées
        if pygame.time.get_ticks() - victory_time > 5000:
            pygame.quit()
            exit()

    if game_over:
        over_surface = text_font.render("GAME OVER", True, (255, 0, 0))
        window.blit(over_surface, (GAME_WIDTH//2 - 100, GAME_HEIGHT//2))

    pygame.display.update()
    clock.tick(60) 