import pygame
import random
import sys
import os

# --- 1. CONFIGURATION INITIALE ---
pygame.init()
WIDTH, HEIGHT = 600, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shifumi : Duel dans la Forêt !")

# Dossier de base (là où se trouve ton fichier .py)
BASE_DIR = os.path.dirname(__file__)

# Couleurs
FOREST_GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 30, 30)
GRAY = (240, 240, 240)

# Polices
font_score = pygame.font.SysFont("Arial", 26, bold=True)
font_main = pygame.font.SysFont("Arial", 22, bold=True)
font_button = pygame.font.SysFont("Arial", 16, bold=True)

# --- 2. FONCTION DE CHARGEMENT SÉCURISÉE ---
def charger_asset(nom_fichier):
    chemin = os.path.join(BASE_DIR, "projet pygame", "images du projet", nom_fichier)
    
    if os.path.exists(chemin):
        return pygame.image.load(chemin)
    else:
        # Si ça ne marche pas, on essaie sans le dossier "projet pygame" au cas où
        chemin_secours = os.path.join(BASE_DIR, "images du projet", nom_fichier)
        if os.path.exists(chemin_secours):
            return pygame.image.load(chemin_secours)
    
    print(f"ALERTE : Image introuvable -> {nom_fichier}")
    return None

# --- 3. CHARGEMENT DES IMAGES ---
# Fond
img_fond_brut = charger_asset("fond pierre feuille ciseaux.jpg")
if img_fond_brut:
    background = pygame.transform.scale(img_fond_brut, (WIDTH, HEIGHT)).convert()
else:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((100, 150, 100))

# Sprites
img_p = charger_asset("pierre.png")
img_pa = charger_asset("papier.png")
img_ci = charger_asset("cisaux.png")

if img_p and img_pa and img_ci:
    icones = {
        "pierre": pygame.transform.scale(img_p, (50, 40)).convert_alpha(),
        "papier": pygame.transform.scale(img_pa, (50, 40)).convert_alpha(),
        "ciseaux": pygame.transform.scale(img_ci, (50, 40)).convert_alpha()
    }
    icones_grandes = {
        "pierre": pygame.transform.scale(img_p, (100, 80)).convert_alpha(),
        "papier": pygame.transform.scale(img_pa, (100, 80)).convert_alpha(),
        "ciseaux": pygame.transform.scale(img_ci, (100, 80)).convert_alpha()
    }
else:
    icones = None

# --- 4. VARIABLES DE JEU ---
valeurs = ["pierre", "papier", "ciseaux"]
score_joueur = 0
score_ordi = 0
SCORE_LIMITE = 5
game_over = False
message_resultat = "Le premier à 5 points gagne !"
choix_joueur, choix_ordi = "", ""

buttons = {
    "pierre": pygame.Rect(50, 350, 150, 60),
    "papier": pygame.Rect(225, 350, 150, 60),
    "ciseaux": pygame.Rect(400, 350, 150, 60)
}

def determiner_gagnant(j, o):
    global score_joueur, score_ordi
    if j == o:
        return f"Egalite ! ({j} vs {o})"
    elif (j == "pierre" and o == "ciseaux") or \
         (j == "papier" and o == "pierre") or \
         (j == "ciseaux" and o == "papier"):
        score_joueur += 1
        return f"Gagne ! {j.capitalize()} bat {o}"
    else:
        score_ordi += 1
        return f"Perdu... {o.capitalize()} bat {j}"

# --- 5. BOUCLE PRINCIPALE ---
running = True
clock = pygame.time.Clock()

while running:
    screen.blit(background, (0, 0))
    
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
            score_joueur, score_ordi = 0, 0
            game_over = False
            choix_joueur, choix_ordi = "", ""
            message_resultat = "C'est reparti !"

    # UI 
    overlay_score = pygame.Surface((WIDTH, 60), pygame.SRCALPHA)
    overlay_score.fill((0, 0, 0, 180))
    screen.blit(overlay_score, (0, 0))
    txt_score = font_score.render(f"Joueur: {score_joueur}  |  Ordi: {score_ordi}", True, WHITE)
    screen.blit(txt_score, (WIDTH//2 - txt_score.get_width()//2, 15))

    if choix_joueur != "" and icones and not game_over:
        screen.blit(icones_grandes[choix_joueur], (100, 180))
        vs_text = font_score.render("VS", True, WHITE)
        screen.blit(vs_text, (WIDTH//2 - vs_text.get_width()//2, 200))
        screen.blit(icones_grandes[choix_ordi], (400, 180))
        
        txt_res = font_main.render(message_resultat, True, WHITE)
        screen.blit(txt_res, (WIDTH//2 - txt_res.get_width()//2, 285))

    # UI : Boutons
    for choix, rect in buttons.items():
        mouse_pos = pygame.mouse.get_pos()
        color = WHITE if rect.collidepoint(mouse_pos) else GRAY
        pygame.draw.rect(screen, color, rect, border_radius=12)
        pygame.draw.rect(screen, FOREST_GREEN, rect, 3, border_radius=12)
        
        if icones:
            screen.blit(icones[choix], (rect.x + 5, rect.y + 10))
            lbl = font_button.render(choix.upper(), True, FOREST_GREEN)
            screen.blit(lbl, (rect.x + 60, rect.y + 20))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(220)
        overlay.fill(WHITE)
        screen.blit(overlay, (0,0))
        
        res_txt = "VICTOIRE tu as sauvé la foret des flames !" if score_joueur >= SCORE_LIMITE else "la foret est perdu..."
        txt_fin = font_score.render(res_txt, True, FOREST_GREEN if score_joueur >= SCORE_LIMITE else RED)
        screen.blit(txt_fin, (WIDTH//2 - txt_fin.get_width()//2, HEIGHT//2 - 20))
        screen.blit(font_main.render("Appuie sur 'R' pour rejouer", True, BLACK), (WIDTH//2 - 120, HEIGHT//2 + 30))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()