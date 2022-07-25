import pygame
import time
import datetime

from music import Music
from sound import SoundManager
from dialog import DialogBox

class Menu:

    def __init__(self):

        # Import de la class music
        self.music = Music()
        self.sound_manager = SoundManager()
        self.dialog_box = DialogBox()

        # Fond d'écran
        self.background = pygame.image.load(f'assets/maps/world.png')
        self.background = pygame.transform.scale(self.background, (800, 700))

        # Bannière (renseigner si souhaité)
        # self.banner = pygame.image.load('assets/menus/banner.png')
        # self.banner = pygame.transform.scale(self.banner, (800, 600))

        # Police de caractère
        self.font = pygame.font.Font(f'assets/dialogs/dialog_font.ttf', 18)

        # Bouton (cadre générique)
        self.button = pygame.image.load('assets/dialogs/dialog_box.png')

        # Flèche
        self.arrow = pygame.image.load('assets/menus/arrow2.png')
        self.arrow = pygame.transform.scale(self.arrow, (50, 50))

        # Panda
        self.panda_img = pygame.transform.scale(pygame.image.load(f'assets/menus/panda_roux.PNG'), (400,400))

        # Index pour savoir où l'on est dans le menu
        self.position_arrow = [400, 250]
        self.index_menu = 1

        # Valeur par défaut pour accéder au jeu
        self.is_playing = False
        self.intro = False
        self.panda_print = False
        self.time_sec = time.time()

        # Musique du menu

    def get_menu(self, screen, inventaire):

        reprendre_partie = inventaire

        # Fenêtre
        self.screen = screen

        # Fond d'écran accueil
        screen.blit(self.background, (0, 0))

        # Bannière (à ajouter si souhaité)

        # Affichage de l'usage des touches
        self.menu_keys(x=30, y=550, screen=self.screen, colorbox = (200,200,200), colortext = (230,230,230))

        # Boutons (avec leur numéros)
        if reprendre_partie:
            self.menu_item(1, "Reprendre la partie")
        else:
            self.menu_item(1, "Nouvelle partie")
        self.menu_item(2, "Charger une partie")
        self.menu_item(3, "Voir un panda roux")
        self.menu_item(4, "Quitter")

        # Position de la flèche
        self.screen.blit(self.arrow, (self.position_arrow[0], self.position_arrow[1]))

        # Affichage du panda
        if self.panda_print:
            screen.blit(self.panda_img, (200, 100))
            pygame.draw.rect(screen, (50, 50, 50), (198, 98, 404, 404), 2, 2, 2, 2)

        # Acutalisation de l'écran
        pygame.display.flip()
        return

    def play(self):
        enter = pygame.key.get_pressed()[pygame.K_RETURN]
        if enter and self.index_menu == 1:
            self.is_playing = True
            self.intro = True
            self.sound_manager.sound_play('click')
            time.sleep(0.2)
            self.music.music_play(origin_world='menu', target_world='house_player2')



    def move_arrow(self):
        pressed = pygame.key.get_pressed()

        if (self.time_sec + .4) < round(time.time()):
            if pressed[pygame.K_DOWN] and self.index_menu < 4:
                self.sound_manager.sound_play('click', volume=0.3)
                self.time_sec = round(time.time())
                self.position_arrow[1] += 75
                self.index_menu += 1

            elif pressed[pygame.K_UP] and self.index_menu > 1 :
                self.sound_manager.sound_play('click', volume=0.3)
                self.time_sec = time.time()
                self.position_arrow[1] -= 75
                self.index_menu -= 1


    def menu_item(self, num, name):
        self.button = pygame.transform.scale(self.button, (300, 50))
        self.button_text = self.font.render(f"{name}", False, (0, 0, 0))
        self.screen.blit(self.button, (450, 175 + (num * 75)))
        self.screen.blit(self.button_text, (450 + 25, 175 + 15 + (num * 75)))

    def menu_keys(self, x, y, screen, colorbox = (50,50,50), colortext = (200,200,200)):

        touche = self.font.render(" -- Partie ------------", False, colortext)
        screen.blit(touche, (x , y + 2-145))

        pygame.draw.rect(screen, colorbox, (x, y-115, 30, 30), 2, 2, 2, 2)
        touche = self.font.render("i    ouvrir inventaire", False, colortext)
        screen.blit(touche, (x+10, y+2-115))

        pygame.draw.rect(screen, colorbox, (x, y-75, 95, 30), 2, 2, 2, 2)
        touche = self.font.render("space    interagir", False, colortext)
        screen.blit(touche, (x+10, y+2-75))

        touche = self.font.render("-- Menu ------------", False, colortext)
        screen.blit(touche, (x, y + 2 - 30))

        pygame.draw.rect(screen, colorbox, (x, y, 95, 30), 2, 2, 2, 2)
        touche = self.font.render("enter    valider", False, colortext)
        screen.blit(touche, (x+10, y+2))



