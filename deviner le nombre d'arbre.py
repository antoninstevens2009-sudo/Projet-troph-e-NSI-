import pygame # type: ignore
import random

# Initialisation
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

# Couleurs
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)

# --- NOUVELLE FONCTION POUR GENERER UN NIVEAU ---
def generer_niveau():
    nb = random.randint(3, 12)
    pos = [(random.randint(50, 750), random.randint(150, 500)) for _ in range(nb)]
    return nb, pos

def dessiner_arbre(x, y):
    pygame.draw.rect(screen, BROWN, (x, y, 20, 40))
    pygame.draw.circle(screen, GREEN, (x + 10, y), 30)

# Variables de progression
manche_actuelle = 1
total_manches = 3
nombre_arbres, positions_arbres = generer_niveau()
input_text = ""
message = f"Manche {manche_actuelle}/{total_manches} : Combien d'arbres ?"
jeu_fini = False

running = True
while running:
    screen.fill((135, 206, 235))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN and not jeu_fini:
            if event.key == pygame.K_RETURN:
                # Vérification de la réponse
                if input_text == str(nombre_arbres):
                    if manche_actuelle < total_manches:
                        # On passe à la manche suivante
                        manche_actuelle += 1
                        nombre_arbres, positions_arbres = generer_niveau()
                        input_text = ""
                        message = f"Bravo ! Manche {manche_actuelle}/{total_manches}"
                    else:
                        # Le joueur a gagné les 3 manches
                        message = "Félicitations ! Tu as gagné le jeu !"
                        jeu_fini = True
                else:
                    message = f"Raté ! C'était {nombre_arbres}. Recommence !"
                    input_text = ""
            
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                if event.unicode.isdigit():
                    input_text += event.unicode

    # Dessin
    for pos in positions_arbres:
        dessiner_arbre(pos[0], pos[1])

    # Interface
    img_msg = font.render(message, True, WHITE)
    img_input = font.render(f"Ta réponse : {input_text}", True, WHITE)
    screen.blit(img_msg, (20, 20))
    if not jeu_fini:
        screen.blit(img_input, (20, 60))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()