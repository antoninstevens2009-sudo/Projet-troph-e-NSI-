# Créé par yangz, le 08/03/2026 en Python 3.7
import pygame
import random
import sys

pygame.init()

WIDTH = 900
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de Calcul")

font = pygame.font.SysFont(None, 70)
medium_font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 36)

# Couleurs
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (70,130,180)
LIGHT_BLUE = (135,206,235)
RED = (220,70,70)
GREEN = (70,200,100)

# Etats
etat = "menu"

niveau = 1
vies = 3

shake_timer = 0


# Calculs

def generer_calcul(niveau):

    if niveau <= 3:

        op = random.choice(["*", "-"])
        a = random.randint(1,10)
        b = random.randint(1,10)

        if op == "*":
            question = f"{a} x {b}"
            rep = a*b
        else:
            question = f"{a} - {b}"
            rep = a-b

    elif niveau <= 6:

        op = random.choice(["*", "/"])

        if op == "*":
            a = random.randint(1,10)
            b = random.randint(1,10)
            question = f"{a} x {b}"
            rep = a*b

        else:
            rep = random.randint(1,10)
            b = random.randint(1,10)
            a = rep*b
            question = f"{a} / {b}"

    else:

        a = random.randint(1,10)
        b = random.randint(1,10)
        c = random.randint(1,10)

        type_calc = random.choice([1,2,3])

        if type_calc == 1:
            question = f"({a} x {b}) + {c}"
            rep = (a*b)+c

        elif type_calc == 2:
            question = f"({a} x {b}) - {c}"
            rep = (a*b)-c

        else:
            question = f"({a} + {b}) x {c}"
            rep = (a+b)*c

    mauvaises = set()

    while len(mauvaises) < 2:

        faux = rep + random.randint(-10,10)

        if faux != rep:
            mauvaises.add(faux)

    choix = [rep] + list(mauvaises)
    random.shuffle(choix)

    return question, rep, choix


# Boutons réponses

def creer_boutons(choix):

    boutons = []

    for i,rep in enumerate(choix):

        rect = pygame.Rect(300,260 + i*90,300,60)

        boutons.append((rect,rep))

    return boutons


question, bonne_rep, choix = generer_calcul(niveau)
boutons = creer_boutons(choix)


# Boutons interface

btn_jouer = pygame.Rect(350,320,200,70)
btn_rejouer = pygame.Rect(300,420,140,60)
btn_quitter = pygame.Rect(460,420,140,60)


# Boucle principale

clock = pygame.time.Clock()
running = True

while running:

    offset_x = 0
    offset_y = 0

    if shake_timer > 0:
        shake_timer -= 1
        offset_x = random.randint(-5,5)
        offset_y = random.randint(-5,5)

    surface = pygame.Surface((WIDTH,HEIGHT))
    surface.fill(LIGHT_BLUE)

    # MENU

    if etat == "menu":

        titre = font.render("JEU DE CALCUL",True,WHITE)
        surface.blit(titre,(WIDTH/2 - titre.get_width()/2,200))

        pygame.draw.rect(surface,BLUE,btn_jouer)

        txt = medium_font.render("JOUER",True,WHITE)
        surface.blit(txt,(btn_jouer.x+45,btn_jouer.y+15))

    # JEU

    elif etat == "jeu":

        niveau_txt = small_font.render(f"Niveau : {niveau}/10",True,BLACK)
        vies_txt = small_font.render(f"Vies : {vies}",True,RED)

        surface.blit(niveau_txt,(20,20))
        surface.blit(vies_txt,(20,60))

        q = font.render(question,True,BLACK)
        surface.blit(q,(WIDTH/2 - q.get_width()/2,150))

        for rect,rep in boutons:

            pygame.draw.rect(surface,BLUE,rect)

            txt = small_font.render(str(rep),True,WHITE)
            surface.blit(txt,(rect.x + rect.width/2 - txt.get_width()/2, rect.y+15))

    # VICTOIRE

    elif etat == "victoire":

        titre = font.render("VICTOIRE",True,GREEN)
        surface.blit(titre,(WIDTH/2 - titre.get_width()/2,200))

        pygame.draw.rect(surface,GREEN,btn_rejouer)
        pygame.draw.rect(surface,RED,btn_quitter)

        txt1 = small_font.render("Rejouer",True,WHITE)
        txt2 = small_font.render("Quitter",True,WHITE)

        surface.blit(txt1,(btn_rejouer.x+25,btn_rejouer.y+18))
        surface.blit(txt2,(btn_quitter.x+30,btn_quitter.y+18))

    # DEFAITE

    elif etat == "defaite":

        titre = font.render("PERDU",True,RED)
        surface.blit(titre,(WIDTH/2 - titre.get_width()/2,200))

        pygame.draw.rect(surface,GREEN,btn_rejouer)
        pygame.draw.rect(surface,RED,btn_quitter)

        txt1 = small_font.render("Rejouer",True,WHITE)
        txt2 = small_font.render("Quitter",True,WHITE)

        surface.blit(txt1,(btn_rejouer.x+25,btn_rejouer.y+18))
        surface.blit(txt2,(btn_quitter.x+30,btn_quitter.y+18))

    screen.blit(surface,(offset_x,offset_y))

    pygame.display.flip()

    # EVENTS

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()

            if etat == "menu":

                if btn_jouer.collidepoint(pos):
                    etat = "jeu"

            elif etat == "jeu":

                for rect,rep in boutons:

                    if rect.collidepoint(pos):

                        if rep == bonne_rep:

                            niveau += 1

                            if niveau > 10:
                                etat = "victoire"

                            else:
                                question, bonne_rep, choix = generer_calcul(niveau)
                                boutons = creer_boutons(choix)

                        else:

                            vies -= 1
                            shake_timer = 15

                            if vies <= 0:
                                etat = "defaite"

            elif etat in ["victoire","defaite"]:

                if btn_rejouer.collidepoint(pos):

                    niveau = 1
                    vies = 3

                    question, bonne_rep, choix = generer_calcul(niveau)
                    boutons = creer_boutons(choix)

                    etat = "jeu"

                if btn_quitter.collidepoint(pos):

                    pygame.quit()
                    sys.exit()

    clock.tick(60)

pygame.quit()
