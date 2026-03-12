import pygame 
import random

# Initialisation
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)
font_chrono = pygame.font.SysFont("Arial", 48, bold=True)

# CHARGEMENT DES IMAGES 
try:
    # Image de fond
    background = pygame.image.load("projet pygame/images du projet/pngtree-inferno-a-3d-render-of-a-forest-ablaze-with-flames-and-image_3677061.jpg").convert()
    background = pygame.transform.scale(background, (800, 600))
    
    # Sprite de l'arbre 
    sprite_arbre = pygame.image.load("projet pygame/images du projet/sprite arbre qui brule.png").convert_alpha()
    sprite_arbre = pygame.transform.scale(sprite_arbre, (200, 250))
except:
    # Surfaces de secours si les images sont manquantes
    background = pygame.Surface((800, 600))
    background.fill((50, 50, 70))
    sprite_arbre = pygame.Surface((150, 200))
    sprite_arbre.fill((200, 50, 0))

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 50, 50)

def generer_niveau():
    # Nombre d'arbres
    nb = random.randint(2, 5)
    # Positions adaptées pour que les pieds des arbres soient sur le sol
    pos = [(random.randint(0, 600), random.randint(200, 350)) for _ in range(nb)]
    pos.sort(key=lambda p: p[1])
    return nb, pos

def dessiner_arbre(x, y):
    vx = random.randint(-1, 1)
    vy = random.randint(-1, 1)
    screen.blit(sprite_arbre, (x + vx, y + vy))

# Variables de jeu
manche_actuelle = 1
total_manches = 3
nombre_arbres, positions_arbres = generer_niveau()
input_text = ""
message = f"Manche {manche_actuelle}/{total_manches} : Vite !"
jeu_fini = False

# Chronomètre
temps_limite = 10
ticks_debut = pygame.time.get_ticks()

running = True
while running:
    # 1. Gestion du temps
    if not jeu_fini:
        secondes_ecoulees = (pygame.time.get_ticks() - ticks_debut) / 1000
        temps_restant = max(0, temps_limite - secondes_ecoulees)
        
        if temps_restant <= 0:
            message = f"Trop tard ! C'était {nombre_arbres}. Recommence !"
            nombre_arbres, positions_arbres = generer_niveau()
            ticks_debut = pygame.time.get_ticks()
            input_text = ""

    # 2. DESSIN DU FOND 
    screen.blit(background, (0, 0))

    # 3. Événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN and not jeu_fini:
            if event.key == pygame.K_RETURN:
                if input_text == str(nombre_arbres):
                    if manche_actuelle < total_manches:
                        manche_actuelle += 1
                        nombre_arbres, positions_arbres = generer_niveau()
                        input_text = ""
                        ticks_debut = pygame.time.get_ticks()
                        message = f"Bravo ! Manche {manche_actuelle}/{total_manches}"
                    else:
                        message = "Félicitations ! La forêt est sauvée !"
                        jeu_fini = True
                else:
                    message = "Faux ! Recompte vite !"
                    input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                if event.unicode.isdigit():
                    input_text += event.unicode

    # 4. Dessin des arbres
    for pos in positions_arbres:
        dessiner_arbre(pos[0], pos[1])

    # 5. Interface
    img_msg = font.render(message, True, WHITE)
    # Petit contour noir pour que le texte soit lisible sur n'importe quel fond
    pygame.draw.rect(screen, (0,0,0, 150), (15, 15, img_msg.get_width() + 10, 40))
    screen.blit(img_msg, (20, 20))
    
    if not jeu_fini:
        img_input = font.render(f"Ta réponse : {input_text}", True, (255, 200, 0))
        screen.blit(img_input, (20, 65))
        
        couleur_chrono = WHITE if temps_restant > 3 else RED
        img_chrono = font_chrono.render(f"{temps_restant:.1f}s", True, couleur_chrono)
        screen.blit(img_chrono, (650, 20))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()