import pygame
import random
import os
def marquer_jeu_gagne(numero):
    jeux_gagnes[numero] = "1"
    with open(fichier_jeux, "w") as f:
        for val in jeux_gagnes:
            f.write(val + "\n")
def lancer_jeu1():
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
    etat = "menu_jeu1"

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
            
                rep = random.randint(1,10)
                b = random.randint(1,10)
                a = rep * b
                question = f"{a} / {b}"

        
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

        if etat == "menu_jeu1":

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

                if etat == "menu_jeu1":

                    if btn_jouer.collidepoint(pos):
                        etat = "jeu"

                elif etat == "jeu":

                    for rect,rep in boutons:

                        if rect.collidepoint(pos):

                            if rep == bonne_rep:

                                niveau += 1

                                if niveau > 10:
                                    marquer_jeu_gagne(0)
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
                        return

        clock.tick(60)

          
def lancer_jeu2():
    import pygame
    import sys
    import random
    import math  # ajouté pour les angles des feuilles

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
        """Dessine un cocotier stylisé (tronc fuselé, feuilles rayonnantes, noix de coco)"""
        # Tronc : polygone trapézoïdal (plus large en bas)
        trunk_bottom_width = 22
        trunk_top_width = 10
        trunk_height = 80

        # Coordonnées du trapèze
        top_left_x = x + (trunk_bottom_width - trunk_top_width) // 2
        top_right_x = x + trunk_bottom_width - (trunk_bottom_width - trunk_top_width) // 2
        bottom_left = (x, y + trunk_height)
        bottom_right = (x + trunk_bottom_width, y + trunk_height)
        top_left = (top_left_x, y)
        top_right = (top_right_x, y)

        pygame.draw.polygon(screen, BROWN, [bottom_left, bottom_right, top_right, top_left])

        # Centre du sommet du tronc (pour placer les feuilles)
        center_top = (x + trunk_bottom_width // 2, y)

        # Feuilles : 7 lignes vertes rayonnant depuis le sommet
        for i in range(7):
            angle = (i - 3) * 15  # de -45° à +45°
            rad = math.radians(angle)
            dx = 45 * math.sin(rad)
            dy = -40 * math.cos(rad)  # négatif car y augmente vers le bas
            end_x = center_top[0] + dx
            end_y = center_top[1] + dy
            # Alterner les teintes de vert pour plus de réalisme
            color = (34, 139, 34) if i % 2 == 0 else (0, 100, 0)
            pygame.draw.line(screen, color, center_top, (end_x, end_y), 3)

        # Quelques feuilles secondaires plus petites (optionnel)
        for i in range(4):
            angle = (i - 1.5) * 20
            rad = math.radians(angle)
            dx = 30 * math.sin(rad)
            dy = -25 * math.cos(rad)
            end_x = center_top[0] + dx
            end_y = center_top[1] + dy
            pygame.draw.line(screen, (0, 120, 0), center_top, (end_x, end_y), 2)

        # Noix de coco
        pygame.draw.circle(screen, BROWN, (center_top[0] - 8, center_top[1] - 12), 6)
        pygame.draw.circle(screen, BROWN, (center_top[0] + 6, center_top[1] - 18), 5)
        pygame.draw.circle(screen, BROWN, (center_top[0] + 12, center_top[1] - 8), 4)
        # Petite ombre sur les noix
        pygame.draw.circle(screen, (101, 67, 33), (center_top[0] - 8, center_top[1] - 12), 3)
        pygame.draw.circle(screen, (101, 67, 33), (center_top[0] + 6, center_top[1] - 18), 2)

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
        # Palmiers (maintenant des cocotiers)
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
        if lvl == 1 or lvl== 2 or lvl== 3:
            a,b = random.randint(1,10), random.randint(1,10)
            return (f"{a}+{b}",a+b) if random.choice([True,False]) else (f"{a}-{b}",a-b)


    # OBJETS

    def create_papers():
        return [pygame.Rect(random.randint(100,700), random.randint(100,500),30,30) for _ in range(3)]

    def create_enemies(lvl):
        enemies=[]
        speed_factor=0.3
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
                marquer_jeu_gagne(1)
                pygame.time.delay(2000)
                return

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
        
def lancer_jeu3():
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
        DOSSIER_BASE = os.path.dirname(__file__)
        DOSSIER_IMAGES = os.path.join(DOSSIER_BASE, "image")
        chemin_bg = os.path.join(DOSSIER_IMAGES, "pngtree-inferno-a-3d-render-of-a-forest-ablaze-with-flames-and-image_3677061.jpg")
        background = pygame.image.load(chemin_bg).convert()  # convert pour optimiser l'affichage
        background = pygame.transform.scale(background, (800, 600))

        # Sprite de l'arbre
        chemin_arbre = os.path.join(DOSSIER_IMAGES, "sprite arbre qui brule.png")
        sprite_arbre = pygame.image.load(chemin_arbre).convert_alpha()  # convert_alpha pour garder la transparence
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
        nb = random.randint(2, 6)
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
                            marquer_jeu_gagne(2)
                            pygame.time.delay(3000)
                            return

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

    
def lancer_jeu4():
    import pygame
    import random
    import sys
    import os

    # --- 1. CONFIGURATION INITIALE ---
    pygame.init()
    WIDTH, HEIGHT = 600, 450
    screen = pygame.display.set_mode((WIDTH, HEIGHT))


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

    # --- 3. CHARGEMENT DES IMAGES ---
    # Fond
    def charger_assets():
        
        try:
            BASE_DIR = os.path.dirname(__file__)
            DOSSIER_IMAGES = os.path.join(BASE_DIR, "image")

            # Fond
            img_fond_brut = pygame.image.load(os.path.join(DOSSIER_IMAGES, "fond pierre feuille ciseaux.jpg")).convert()
            background = pygame.transform.scale(img_fond_brut, (WIDTH, HEIGHT))

            # Sprites
            img_p = pygame.image.load(os.path.join(DOSSIER_IMAGES, "pierre.png")).convert_alpha()
            img_pa = pygame.image.load(os.path.join(DOSSIER_IMAGES, "papier.png")).convert_alpha()
            img_ci = pygame.image.load(os.path.join(DOSSIER_IMAGES, "ciseaux.png")).convert_alpha()

            # Icônes normales
            icones = {
                "pierre": pygame.transform.scale(img_p, (50, 40)),
                "papier": pygame.transform.scale(img_pa, (50, 40)),
                "ciseaux": pygame.transform.scale(img_ci, (50, 40))
            }

            # Icônes grandes
            icones_grandes = {
                "pierre": pygame.transform.scale(img_p, (100, 80)),
                "papier": pygame.transform.scale(img_pa, (100, 80)),
                "ciseaux": pygame.transform.scale(img_ci, (100, 80))
            }

        except Exception as e:
            print(f"ALERTE : Problème de chargement des images -> {e}")

            # Fond de secours
            background = pygame.Surface((WIDTH, HEIGHT))
            background.fill((100, 150, 100))

            # Icônes de secours dessinées
            icones = {}
            icones_grandes = {}

            # Pierre : carré gris
            surf_p = pygame.Surface((50, 40), pygame.SRCALPHA)
            pygame.draw.rect(surf_p, (150, 150, 150), (0, 0, 50, 40))
            icones["pierre"] = surf_p
            icones_grandes["pierre"] = pygame.transform.scale(surf_p, (100, 80))

            # Papier : rectangle blanc
            surf_pa = pygame.Surface((50, 40), pygame.SRCALPHA)
            pygame.draw.rect(surf_pa, (255, 255, 255), (0, 0, 50, 40))
            icones["papier"] = surf_pa
            icones_grandes["papier"] = pygame.transform.scale(surf_pa, (100, 80))

            # Ciseaux : triangle rouge
            surf_ci = pygame.Surface((50, 40), pygame.SRCALPHA)
            pygame.draw.polygon(surf_ci, (255, 0, 0), [(0,40),(25,0),(50,40)])
            icones["ciseaux"] = surf_ci
            icones_grandes["ciseaux"] = pygame.transform.scale(surf_ci, (100, 80))
        return background, icones, icones_grandes

    background, icones, icones_grandes = charger_assets()


        

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
        nonlocal score_joueur, score_ordi  
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

            if score_joueur >= SCORE_LIMITE:
                marquer_jeu_gagne(3)
                screen.blit(font_main.render("Bravo", True, BLACK), (WIDTH//2 - 120, HEIGHT//2 + 30))
                pygame.display.flip()   # nécessaire pour afficher avant le wait
                pygame.time.wait(2000)  # pause de 4 secondes
                WIDTH, HEIGHT = 800,600
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                return  # quitte le jeu après la victoire

            # Si défaite, juste affiche le message et laisse le joueur appuyer sur R
            screen.blit(font_main.render("Appuie sur 'R' pour rejouer", True, BLACK), (WIDTH//2 - 120, HEIGHT//2 + 30))    
                

        pygame.display.flip()
        clock.tick(30)

    return

pygame.init()

DOSSIER_BASE = os.path.dirname(__file__)
LARGEUR, HAUTEUR = 800, 600
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.RESIZABLE)
pygame.display.set_caption("Main")

image_bouton_puzzle = pygame.image.load(os.path.join(DOSSIER_BASE, "image", "image_bouton_puzzle.jpg"))
image_bouton_puzzle = pygame.transform.scale(image_bouton_puzzle, (80, 80))
image_sapin = pygame.image.load(os.path.join(DOSSIER_BASE, "image", "image_sapin.jpg"))
image_sapin = pygame.transform.scale(image_sapin, (20, 20))
image_puzzle = pygame.image.load(os.path.join(DOSSIER_BASE, "image", "image_puzzle.jpg"))
image_puzzle = pygame.transform.scale(image_puzzle, (600, 400))

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
    vitesse = random.uniform(0.3, 1.2)
    liste_sapins.append([x, y, vitesse])

boutons_jeux = [
    [pygame.Rect(150, 200, 200, 80), "Jeu 1"],
    [pygame.Rect(450, 200, 200, 80), "Jeu 2"],
    [pygame.Rect(150, 320, 200, 80), "Jeu 3"],
    [pygame.Rect(450, 320, 200, 80), "Jeu 4"],
    [pygame.Rect(150, 440, 200, 80), "Jeu 5"],
    [pygame.Rect(450, 440, 200, 80), "Jeu 6"]
]

bouton_puzzle_rect = image_bouton_puzzle.get_rect(topleft=(20, 20))
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
                    ecran = "puzzle"
                for b, nom in boutons_jeux:
                    if b.collidepoint(evenement.pos):

                        if nom == "Jeu 1":
                            lancer_jeu1()
                        if nom == "Jeu 2":
                            lancer_jeu2()
                        if nom == "Jeu 3":
                            lancer_jeu3()
                        if nom == "Jeu 4":
                            lancer_jeu4()
                if bouton_regles.collidepoint(evenement.pos):
                    ecran = "regles"
            elif ecran == "regles":
                if bouton_retour.collidepoint(evenement.pos):
                    ecran = "menu"
            elif ecran == "puzzle":
                if bouton_retour.collidepoint(evenement.pos):
                    ecran = "menu"
            elif ecran == "gagne":
                if bouton_retour.collidepoint(evenement.pos):
                    ecran = "menu"

    fenetre.fill(BLEU)
    for sapin in liste_sapins:
        fenetre.blit(image_sapin, (sapin[0], sapin[1]))
        sapin[1] = sapin[2] + sapin[1]
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

    elif ecran == "puzzle":
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
        carre_largeur = image_puzzle.get_width() // 3
        carre_hauteur = image_puzzle.get_height() // 2

        if jeux_gagnes[0] == "1" and jeux_gagnes[1] == "1" and jeux_gagnes[2] == "1" and \
           jeux_gagnes[3] == "1" and jeux_gagnes[4] == "1" and jeux_gagnes[5] == "1":
            ecran = "gagne"

        if jeux_gagnes[0] == "0":
            pygame.draw.rect(fenetre, ROUGE, (puzzle_x + 0*carre_largeur, puzzle_y + 0*carre_hauteur, carre_largeur, carre_hauteur))
        if jeux_gagnes[1] == "0":
            pygame.draw.rect(fenetre, ROUGE, (puzzle_x + 1*carre_largeur, puzzle_y + 0*carre_hauteur, carre_largeur, carre_hauteur))
        if jeux_gagnes[2] == "0":
            pygame.draw.rect(fenetre, ROUGE, (puzzle_x + 2*carre_largeur, puzzle_y + 0*carre_hauteur, carre_largeur, carre_hauteur))
        if jeux_gagnes[3] == "0":
            pygame.draw.rect(fenetre, ROUGE, (puzzle_x + 0*carre_largeur, puzzle_y + 1*carre_hauteur, carre_largeur, carre_hauteur))
        if jeux_gagnes[4] == "0":
            pygame.draw.rect(fenetre, ROUGE, (puzzle_x + 1*carre_largeur, puzzle_y + 1*carre_hauteur, carre_largeur, carre_hauteur))
        if jeux_gagnes[5] == "0":
            pygame.draw.rect(fenetre, ROUGE, (puzzle_x + 2*carre_largeur, puzzle_y + 1*carre_hauteur, carre_largeur, carre_hauteur))

    elif ecran == "gagne":
        fenetre.fill(BLANC)
        texte_gagne = pygame.font.SysFont(None, 80).render("Vous avez gagné !", True, BLEU)
        fenetre.blit(texte_gagne, ((LARGEUR - texte_gagne.get_width()) // 2, (HAUTEUR - texte_gagne.get_height()) // 2))
        pygame.draw.rect(fenetre, GRIS, bouton_retour, border_radius=10)
        texte_retour = police.render("Retour", True, BLEU)
        fenetre.blit(texte_retour, (
            bouton_retour.x + (bouton_retour.width - texte_retour.get_width()) // 2,
            bouton_retour.y + (bouton_retour.height - texte_retour.get_height()) // 2
        ))

    pygame.display.flip()

pygame.quit()
