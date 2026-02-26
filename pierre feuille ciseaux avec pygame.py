import pygame
import random
import sys

# --- 1. CONFIGURATION INITIALE ---
pygame.init()

WIDTH, HEIGHT = 600, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pierre - Papier - Ciseaux : Défi dans la Forêt")

# Couleurs "Nature"
LIGHT_GREEN = (144, 238, 144)  # Vert clair pour le fond
FOREST_GREEN = (34, 139, 34)   # Vert foncé pour les détails
BROWN        = (139, 69, 19)    # Marron pour les troncs
BLACK        = (0, 0, 0)
WHITE        = (255, 255, 255)
GRAY         = (240, 240, 240)
RED          = (200, 30, 30)

# Polices
font_score = pygame.font.SysFont("Arial", 26, bold=True)
font_main = pygame.font.SysFont("Arial", 22, bold=True)
font_button = pygame.font.SysFont("Arial", 18, bold=True)

# Variables de jeu
valeurs = ["pierre", "papier", "ciseaux"]
score_joueur = 0
score_ordi = 0
nul = 0
SCORE_LIMITE = 5
game_over = False
message_resultat = "Le premier à 5 points gagne !"
choix_joueur, choix_ordi = "", ""

# Boutons
buttons = {
    "pierre": pygame.Rect(50, 350, 150, 50),
    "papier": pygame.Rect(225, 350, 150, 50),
    "ciseaux": pygame.Rect(400, 350, 150, 50)
}

def determiner_gagnant(j, o):
    global score_joueur, score_ordi, nul
    if j == o:
        nul += 1
        return f"Égalité ! ({j} vs {o})"
    elif (j == "pierre" and o == "ciseaux") or \
         (j == "papier" and o == "pierre") or \
         (j == "ciseaux" and o == "papier"):
        score_joueur += 1
        return f"Gagné ! {j.capitalize()} bat {o}"
    else:
        score_ordi += 1
        return f"Perdu... {o.capitalize()} bat {j}"

# --- 2. BOUCLE PRINCIPALE ---
running = True
while running:
    # --- DESSIN DU FOND "FORÊT" ---
    screen.fill(LIGHT_GREEN)
    
    # Petites décorations pour évoquer la forêt (cercles = feuillage)
    pygame.draw.circle(screen, FOREST_GREEN, (50, 450), 100)
    pygame.draw.circle(screen, FOREST_GREEN, (550, 450), 120)
    pygame.draw.circle(screen, (100, 200, 100), (300, 480), 80)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            for choix, rect in buttons.items():
                if rect.collidepoint(event.pos):
                    choix_joueur, choix_ordi = choix, random.choice(valeurs)
                    message_resultat = determiner_gagnant(choix_joueur, choix_ordi)
                    if score_joueur >= SCORE_LIMITE or score_ordi >= SCORE_LIMITE:
                        game_over = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            score_joueur, score_ordi, nul = 0, 0, 0
            game_over = False
            message_resultat = "C'est reparti dans la forêt !"

    # --- AFFICHAGE ---
    # Score
    txt_score = font_score.render(f"Joueur: {score_joueur} | Ordi: {score_ordi}", True, BLACK)
    screen.blit(txt_score, (WIDTH//2 - txt_score.get_width()//2, 20))

    # Résultat du tour
    txt_res = font_main.render(message_resultat, True, BLACK)
    # Petit contour blanc derrière le texte pour la lisibilité
    screen.blit(txt_res, (WIDTH//2 - txt_res.get_width()//2, 150))

    # Boutons
    for choix, rect in buttons.items():
        color = GRAY if not rect.collidepoint(pygame.mouse.get_pos()) else WHITE
        pygame.draw.rect(screen, color, rect, border_radius=15)
        pygame.draw.rect(screen, FOREST_GREEN, rect, 3, border_radius=15)
        
        lbl = font_button.render(choix.upper(), True, FOREST_GREEN)
        screen.blit(lbl, (rect.x + (rect.width//2 - lbl.get_width()//2), 
                          rect.y + (rect.height//2 - lbl.get_height()//2)))

    # Écran de fin
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(WHITE)
        screen.blit(overlay, (0,0))
        
        gagnant = "TU AS DOMINÉ LA FORÊT !" if score_joueur >= SCORE_LIMITE else "L'ORDI EST LE ROI DU BOIS..."
        txt_fin = font_score.render(gagnant, True, FOREST_GREEN if score_joueur >= SCORE_LIMITE else RED)
        screen.blit(txt_fin, (WIDTH//2 - txt_fin.get_width()//2, HEIGHT//2 - 20))
        
        txt_r = font_main.render("Appuie sur 'R' pour rejouer", True, BLACK)
        screen.blit(txt_r, (WIDTH//2 - txt_r.get_width()//2, HEIGHT//2 + 30))

    pygame.display.flip()

pygame.quit()



