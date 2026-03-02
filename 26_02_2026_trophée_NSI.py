# Créé par yangz, le 26/02/2026 en Python 3.7
import pygame
import sys
import random

pygame.init()


# CONFIG

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tresor sur la plage")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 56)


# COULEURS

SAND = (240, 220, 170)
BLUE = (50, 120, 255)
SKIN = (255, 220, 180)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
RED = (200, 50, 50)
YELLOW = (255, 255, 0)      # pour le chapeau
BROWN = (139, 69, 19)       # pour le ruban du chapeau
WHITE = (255, 255, 255)     # pour les lunettes
DARK_BLUE = (0, 0, 255)     # pour les rayures du maillot
LIGHT_BROWN = (210, 180, 140)  # pour les troncs
PINK = (255, 182, 193)      # pour les coquillages

PLAYER_W, PLAYER_H = 40, 65
speed = 5


# DÉCORS DE PLAGE

def draw_palm_tree(x, y):
    """Dessine un palmier stylisé"""
    # Tronc
    pygame.draw.rect(screen, BROWN, (x, y, 20, 80))
    # Feuilles (triangles verts)
    feuilles1 = [(x-20, y-20), (x+40, y-20), (x+10, y-60)]
    pygame.draw.polygon(screen, GREEN, feuilles1)
    feuilles2 = [(x-10, y-30), (x+30, y-30), (x+10, y-70)]
    pygame.draw.polygon(screen, (0, 150, 0), feuilles2)
    # Noix de coco (optionnelle)
    pygame.draw.circle(screen, DARK_BLUE, (x+10, y+20), 5)

def draw_parasol(x, y):
    """Dessine un parasol de plage"""
    # Pied
    pygame.draw.line(screen, BLACK, (x+15, y), (x+15, y-40), 3)
    # Toit (demi-cercle rayé)
    for i in range(6):
        color = RED if i % 2 == 0 else WHITE
        pygame.draw.arc(screen, color, (x, y-60, 30, 40), 3.14, 0, 3)

def draw_seagull(x, y):
    """Dessine une mouette simplifiée"""
    # Corps
    pygame.draw.ellipse(screen, WHITE, (x, y, 20, 10))
    # Ailes
    pygame.draw.line(screen, WHITE, (x+5, y+2), (x-5, y-5), 3)
    pygame.draw.line(screen, WHITE, (x+15, y+2), (x+25, y-5), 3)
    # Tête
    pygame.draw.circle(screen, WHITE, (x+18, y-2), 3)
    # Bec
    pygame.draw.line(screen, YELLOW, (x+20, y-4), (x+23, y-6), 2)

def draw_shell(x, y):
    """Dessine un petit coquillage"""
    pygame.draw.ellipse(screen, PINK, (x, y, 15, 8))
    pygame.draw.ellipse(screen, WHITE, (x+3, y+2, 5, 3))
    pygame.draw.ellipse(screen, WHITE, (x+8, y+1, 5, 3))

def draw_decorations():
    """Place tous les décors sur la plage"""
    # Palmiers
    draw_palm_tree(100, 450)
    draw_palm_tree(650, 470)
    # Parasols
    draw_parasol(200, 500)
    draw_parasol(500, 520)
    # Mouettes
    draw_seagull(600, 100)
    draw_seagull(650, 150)
    draw_seagull(700, 120)
    # Coquillages
    draw_shell(50, 550)
    draw_shell(750, 530)
    draw_shell(400, 580)


# INIT JEU

def init_game():
    return {
        "player_x": 100,
        "player_y": 100,
        "game_state": "start",
        "level": 1,
        "show_math": False,
        "question": "",
        "current_answer": 0,
        "user_answer": "",
        "papers_solved": 0,
        "error_message": "",
        "error_time": 0,
        "result": ""
    }

game = init_game()


# JOUEUR ANIMÉ ET DÉCORÉ

def draw_player(x, y, moving, frame):
    # Tête
    pygame.draw.circle(screen, SKIN, (x + 20, y + 10), 10)

    # Lunettes de soleil
    pygame.draw.rect(screen, BLACK, (x + 12, y + 6, 6, 4))
    pygame.draw.rect(screen, BLACK, (x + 22, y + 6, 6, 4))
    pygame.draw.line(screen, BLACK, (x + 18, y + 8), (x + 22, y + 8), 2)
    pygame.draw.circle(screen, WHITE, (x + 15, y + 7), 2)
    pygame.draw.circle(screen, WHITE, (x + 25, y + 7), 2)

    # Bouche
    if moving:
        pygame.draw.arc(screen, BLACK, (x + 15, y + 12, 10, 5), 3.14, 0, 2)
    else:
        pygame.draw.arc(screen, BLACK, (x + 15, y + 12, 10, 5), 0, 3.14, 2)

    # Chapeau de paille
    chapeau_points = [(x + 10, y), (x + 30, y), (x + 20, y - 15)]
    pygame.draw.polygon(screen, YELLOW, chapeau_points)
    pygame.draw.line(screen, BROWN, (x + 10, y - 2), (x + 30, y - 2), 3)

    # Corps (maillot de bain rayé)
    pygame.draw.rect(screen, BLUE, (x + 10, y + 20, 20, 30))
    for i in range(3):
        pygame.draw.line(screen, WHITE, (x + 10, y + 25 + i*8), (x + 30, y + 25 + i*8), 2)

    # Bras animés
    offset = 5 if moving and frame % 20 < 10 else -5 if moving else 0
    pygame.draw.line(screen, SKIN, (x + 10, y + 30), (x + 5 + offset, y + 40), 4)
    pygame.draw.line(screen, SKIN, (x + 30, y + 30), (x + 35 - offset, y + 40), 4)

    # Jambes
    pygame.draw.line(screen, BLACK, (x + 15, y + 50), (x + 10 + offset, y + 65), 3)
    pygame.draw.line(screen, BLACK, (x + 25, y + 50), (x + 30 - offset, y + 65), 3)

    # Mains
    pygame.draw.circle(screen, SKIN, (x + 5 + offset, y + 40), 3)
    pygame.draw.circle(screen, SKIN, (x + 35 - offset, y + 40), 3)


# ENNEMI VISUEL

def draw_enemy(rect):
    x, y = rect.x, rect.y
    pygame.draw.ellipse(screen, (120, 0, 120), (x, y, 40, 40))
    pygame.draw.circle(screen, (255,255,255), (x+12,y+15),5)
    pygame.draw.circle(screen, (255,255,255), (x+28,y+15),5)
    pygame.draw.circle(screen, BLACK, (x+12,y+15),2)
    pygame.draw.circle(screen, BLACK, (x+28,y+15),2)
    pygame.draw.arc(screen, BLACK, (x+10,y+18,20,15), 3.14, 0, 2)


# COFFRE VISUEL

def draw_chest(rect):
    x, y = rect.x, rect.y
    pygame.draw.rect(screen, (139,69,19), (x,y+10,30,20))
    pygame.draw.rect(screen, (160,82,45), (x,y,30,15))
    pygame.draw.rect(screen, (255,215,0), (x+12,y+18,6,6))


# MATHS

def generate_math(lvl):
    if lvl == 1:
        a,b = random.randint(1,10), random.randint(1,10)
        return (f"{a}+{b}",a+b) if random.choice([True,False]) else (f"{a}-{b}",a-b)
    if lvl == 2:
        a,b = random.randint(2,9), random.randint(2,9)
        return f"{a}x{b}", a*b
    a,b,c = random.randint(1,5),random.randint(1,5),random.randint(1,5)
    return f"({a}+{b})x{c}", (a+b)*c


# OBJETS

def create_papers():
    return [pygame.Rect(random.randint(100,700), random.randint(100,500),30,30) for _ in range(3)]

def create_enemies(lvl):
    enemies=[]
    speed_factor=1
    for _ in range(lvl+1):
        enemies.append({
            "rect":pygame.Rect(random.randint(100,700), random.randint(100,500),40,40),
            "vx":random.choice([-3,-2,2,3])*speed_factor,
            "vy":random.choice([-3,-2,2,3])*speed_factor
        })
    return enemies

def reset_level(lvl):
    return create_papers(), create_enemies(lvl)

papers,enemies = reset_level(game["level"])
current_paper=None

animation_frame=0
moving=False


# BOUCLE PRINCIPALE

while True:
    # Fond de base (sable)
    screen.fill(SAND)

    # Dessiner les décorations de plage (en arrière-plan)
    draw_decorations()

    # START
    if game["game_state"]=="start":
        screen.blit(big_font.render("Tresor sur la plage",True,BLACK),(220,220))
        screen.blit(font.render("Appuie sur ENTREE",True,GREEN),(270,300))

        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_RETURN:
                game["game_state"]="play"

        pygame.display.flip(); clock.tick(60); continue

    # FIN
    if game["game_state"]=="end":
        color = RED if game["result"]=="GAME OVER" else GREEN
        screen.blit(big_font.render(game["result"],True,color),(260,230))
        screen.blit(font.render("R recommencer | Q quitter",True,BLACK),(190,320))

        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_r:
                    game=init_game()
                    papers,enemies=reset_level(game["level"])
                    current_paper=None
                if e.key==pygame.K_q:
                    pygame.quit(); sys.exit()

        pygame.display.flip(); clock.tick(60); continue

    # EVENTS
    for e in pygame.event.get():
        if e.type==pygame.QUIT: pygame.quit(); sys.exit()

        if game["show_math"] and e.type==pygame.KEYDOWN:
            if e.key==pygame.K_RETURN:
                if game["user_answer"]==str(game["current_answer"]):
                    game["papers_solved"]+=1
                    papers.remove(current_paper)
                    current_paper=None
                    game["show_math"]=False
                    game["user_answer"]=""
                else:
                    game["error_message"]="Mauvaise reponse"
                    game["error_time"]=pygame.time.get_ticks()
                    game["user_answer"]=""

            elif e.key==pygame.K_BACKSPACE:
                game["user_answer"]=game["user_answer"][:-1]
            else:
                if e.unicode.isdigit() or e.unicode=="-":
                    game["user_answer"]+=e.unicode

        if e.type==pygame.KEYDOWN and e.key==pygame.K_SPACE and not game["show_math"]:
            player_rect=pygame.Rect(game["player_x"],game["player_y"],PLAYER_W,PLAYER_H)
            for paper in papers:
                if player_rect.colliderect(paper):
                    game["question"],game["current_answer"]=generate_math(game["level"])
                    game["show_math"]=True
                    current_paper=paper

    # DEPLACEMENTS + ANIMATION
    moving=False
    if not game["show_math"]:
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_q]: game["player_x"]-=speed; moving=True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: game["player_x"]+=speed; moving=True
        if keys[pygame.K_UP] or keys[pygame.K_z]: game["player_y"]-=speed; moving=True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: game["player_y"]+=speed; moving=True
    if moving: animation_frame+=1

    # ENNEMIS
    for enemy in enemies:
        enemy["rect"].x+=enemy["vx"]
        enemy["rect"].y+=enemy["vy"]

        if enemy["rect"].left<=0 or enemy["rect"].right>=WIDTH: enemy["vx"]*=-1
        if enemy["rect"].top<=0 or enemy["rect"].bottom>=HEIGHT: enemy["vy"]*=-1

        if pygame.Rect(game["player_x"],game["player_y"],PLAYER_W,PLAYER_H).colliderect(enemy["rect"]):
            game["result"]="GAME OVER"
            game["game_state"]="end"

    # NIVEAU
    if game["papers_solved"]==3:
        game["level"]+=1
        game["papers_solved"]=0
        if game["level"]>3:
            game["result"]="VICTOIRE"
            game["game_state"]="end"
        else:
            papers,enemies=reset_level(game["level"])
            game["player_x"],game["player_y"]=100,100

    # DESSIN DES ÉLÉMENTS PRINCIPAUX (par-dessus les décors)
    draw_player(game["player_x"],game["player_y"],moving,animation_frame)

    for paper in papers:
        draw_chest(paper)

    for enemy in enemies:
        draw_enemy(enemy["rect"])

    screen.blit(font.render(f"Niveau {game['level']}",True,BLACK),(10,10))

    if game["show_math"]:
        screen.blit(font.render(f"Calcul : {game['question']}",True,BLACK),(200,200))
        screen.blit(font.render(f"Reponse : {game['user_answer']}",True,BLACK),(200,240))

    if game["error_message"] and pygame.time.get_ticks()-game["error_time"]<1500:
        screen.blit(font.render(game["error_message"],True,RED),(200,280))

    pygame.display.flip()
    clock.tick(60)
