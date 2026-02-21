import pygame
import random
import os
pygame.init()
DOSSIER_BASE = os.path.dirname(__file__)
LARGEUR, HAUTEUR = 800, 600
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.RESIZABLE)
pygame.display.set_caption("Main")
image_bouton_puzzle = pygame.image.load(os.path.join(DOSSIER_BASE, "image", "image_bouton_puzzle.jpg"))
image_bouton_puzzle = pygame.transform.scale(image_bouton_puzzle, (80,80))
image_sapin = pygame.image.load(os.path.join(DOSSIER_BASE, "image", "image_sapin.jpg"))
image_sapin = pygame.transform.scale(image_sapin, (20,20))
image_puzzle = pygame.image.load(os.path.join(DOSSIER_BASE, "image", "image_puzzle.jpg"))
image_puzzle = pygame.transform.scale(image_puzzle, (600,400))
liste_sapins = []
fichier_jeux = os.path.join(DOSSIER_BASE, "jeux_gagnes.txt")
if not os.path.exists(fichier_jeux):
    with open(fichier_jeux, "w") as f:
        for i in range(6):
            f.write("0\n")
jeux_gagnes = []
with open(fichier_jeux, "r") as f:
    for ligne in f:
        jeux_gagnes.append(ligne.strip()) 
for i in range(30):
    x = random.randint(10, LARGEUR-20)
    y = random.randint(-HAUTEUR, 0)
    vitesse = random.uniform(0.3,1.2)
    liste_sapins.append([x, y, vitesse])

boutons_jeux = [
    [pygame.Rect(150, 200, 200, 80), "Jeu 1"],
    [pygame.Rect(450, 200, 200, 80), "Jeu 2"],
    [pygame.Rect(150, 320, 200, 80), "Jeu 3"],
    [pygame.Rect(450, 320, 200, 80), "Jeu 4"],
    [pygame.Rect(150, 440, 200, 80), "Jeu 5"],
    [pygame.Rect(450, 440, 200, 80), "Jeu 6"]
]



bouton_puzzle_rect = image_bouton_puzzle.get_rect(topleft=(20,20))
bouton_regles = pygame.Rect(600, 20, 170, 50)
bouton_retour = pygame.Rect(600, 500, 150, 50)

police = pygame.font.SysFont(None, 50)
police_texte_intro = pygame.font.SysFont(None, 36)
BLANC = (255, 255, 255)
BLEU = (50, 50, 200)
GRIS = (200, 200, 200)
ROUGE = (255, 0, 0)
en_cours = True
ecran = "menu"

texte_regles = [
    "Bienvenue dans le jeu !",
    "Faite les jeux un à un",
    "gagnez des pièces de puzzles à chaque fin de jeu",
    "assemblez le puzzle",
    "Gagnez"
]

while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False
        elif evenement.type == pygame.VIDEORESIZE:
            LARGEUR, HAUTEUR = evenement.w, evenement.h
            fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.RESIZABLE)
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            if ecran == "menu":
                if bouton_puzzle_rect.collidepoint(evenement.pos):
                    ecran="puzzle"
                for b, nom in boutons_jeux:
                    if b.collidepoint(evenement.pos):
                        ecran=nom
                if bouton_regles.collidepoint(evenement.pos):
                    ecran = "regles"
            elif ecran == "regles":
                if bouton_retour.collidepoint(evenement.pos):
                    ecran = "menu"
            elif ecran=="puzzle":
                if bouton_retour.collidepoint(evenement.pos):
                    ecran="menu"
            elif ecran=="gagne":
                if bouton_retour.collidepoint(evenement.pos):
                    ecran="menu"


    fenetre.fill(BLEU)

    for sapin in liste_sapins:
        fenetre.blit(image_sapin, (sapin[0], sapin[1]))
        sapin[1] = sapin[2]+sapin[1]
        if sapin[1] > HAUTEUR:
            sapin[1] = random.randint(-HAUTEUR, 0)
            sapin[0] = random.randint(10, LARGEUR-20)

    if ecran == "menu":
        for b, nom in boutons_jeux:
            pygame.draw.rect(fenetre, GRIS, b, border_radius=10)
            texte = police.render(nom, True, BLEU)
            text_x = b.x + (b.width - texte.get_width()) // 2
            text_y = b.y + (b.height - texte.get_height()) // 2
            fenetre.blit(texte, (text_x, text_y))

        fenetre.blit(image_bouton_puzzle, bouton_puzzle_rect)

        pygame.draw.rect(fenetre, GRIS, bouton_regles, border_radius=10)
        texte_r = police.render("Règles du jeu", True, BLEU)
        fenetre.blit(texte_r, (
            bouton_regles.x + (bouton_regles.width - texte_r.get_width()) // 2,
            bouton_regles.y + (bouton_regles.height - texte_r.get_height()) // 2
        ))

    elif ecran == "regles":
        y_pos = 50
        for ligne in texte_regles:
            texte_ligne = police_texte_intro.render(ligne, True, BLANC)
            fenetre.blit(texte_ligne, (50, y_pos))
            y_pos += 50

        pygame.draw.rect(fenetre, GRIS, bouton_retour, border_radius=10)
        texte_retour = police.render("Retour", True, BLEU)
        fenetre.blit(texte_retour, (
            bouton_retour.x + (bouton_retour.width - texte_retour.get_width()) // 2,
            bouton_retour.y + (bouton_retour.height - texte_retour.get_height()) // 2
        ))
    elif ecran=="puzzle":
        fenetre.fill(BLANC)
        pygame.draw.rect(fenetre, GRIS, bouton_retour, border_radius=10)
        texte_retour = police.render("Retour", True, BLEU)
        fenetre.blit(texte_retour, (
            bouton_retour.x + (bouton_retour.width - texte_retour.get_width()) // 2,
            bouton_retour.y + (bouton_retour.height - texte_retour.get_height()) // 2
        ))
        puzzle_x = (LARGEUR - image_puzzle.get_width()) // 2
        puzzle_y = (HAUTEUR - image_puzzle.get_height()) // 2
        fenetre.blit(image_puzzle, (puzzle_x, puzzle_y))
        carre_largeur= image_puzzle.get_width()//3
        carre_hauteur=image_puzzle.get_height()//2
        if jeux_gagnes[0]=="1" and jeux_gagnes[1]=="1" and jeux_gagnes[2]=="1" and jeux_gagnes[3]=="1" and jeux_gagnes[4]=="1" and  jeux_gagnes[5]=="1":
            ecran="gagne"
        if jeux_gagnes[0]=="0":
            pygame.draw.rect(fenetre, ROUGE, (puzzle_x + 0*carre_largeur, puzzle_y + 0*carre_hauteur, carre_largeur, carre_hauteur))
        if jeux_gagnes[1]=="0":
            pygame.draw.rect(fenetre, ROUGE, (puzzle_x + 1*carre_largeur, puzzle_y + 0*carre_hauteur, carre_largeur, carre_hauteur))
        if jeux_gagnes[2]=="0":
            pygame.draw.rect(fenetre, ROUGE, (puzzle_x + 2*carre_largeur, puzzle_y + 0*carre_hauteur, carre_largeur, carre_hauteur))
        if jeux_gagnes[3]=="0":
            pygame.draw.rect(fenetre, ROUGE, (puzzle_x + 0*carre_largeur, puzzle_y + 1*carre_hauteur, carre_largeur, carre_hauteur))
        if jeux_gagnes[4]=="0":
            pygame.draw.rect(fenetre, ROUGE, (puzzle_x + 1*carre_largeur, puzzle_y + 1*carre_hauteur, carre_largeur, carre_hauteur))
        if jeux_gagnes[5]=="0":
            pygame.draw.rect(fenetre, ROUGE, (puzzle_x + 2*carre_largeur, puzzle_y + 1*carre_hauteur, carre_largeur, carre_hauteur))            
    elif ecran=="gagne":
        fenetre.fill(BLANC)
        texte_gagne = pygame.font.SysFont(None, 80).render("Vous avez gagné !", True, BLEU)
        fenetre.blit(texte_gagne, ((LARGEUR - texte_gagne.get_width())//2, (HAUTEUR - texte_gagne.get_height())//2))
    
        pygame.draw.rect(fenetre, GRIS, bouton_retour, border_radius=10)
        texte_retour = police.render("Retour", True, BLEU)
        fenetre.blit(texte_retour, (
            bouton_retour.x + (bouton_retour.width - texte_retour.get_width()) // 2,
            bouton_retour.y + (bouton_retour.height - texte_retour.get_height()) // 2
        ))        
    pygame.display.flip()
pygame.QUIT