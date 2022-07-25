import pygame
import pytmx
import pyscroll

from dialog import DialogBox
from map import MapManager
from player import Player
from menu import Menu
from music import Music
from sound import SoundManager
from inventory import Inventory




class Game:

    def __init__(self):

        # Création fenêtre
        self.inventory = Inventory()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Dr Mind")

        # récupération du menu d'accueil + musique
        self.menu = Menu()
        self.music = Music()
        self.sound = SoundManager()

        # Générer un joueur
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)
        self.dialog_box = DialogBox()

        # Mot de passe de départ
        self.mdp = " ... Aucun checkpoint atteint ..."

    # Gestion des touches
    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

    def update(self):
        self.map_manager.update()

    def run(self):

        # Def des fps
        clock = pygame.time.Clock()

        # Boucle du jeu (maintien de la fenêtre)
        running = True

        if self.menu.is_playing == False:
            self.music.music_play()

        while running:

            if self.menu.is_playing == True:
                self.player.save_location()
                self.handle_input()
                self.update()
                self.map_manager.draw()
                self.inventory.inventory_open_close(self.screen, self.mdp)
                self.dialog_box.render(self.screen)
                self.dialog_box.execute_intro(self.screen)

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            pygame.mixer.music.set_volume(0.1)
                            self.map_manager.check_npc_collisions(self.dialog_box)
                        elif event.key == pygame.K_i:
                            if self.inventory.open_invent == True:
                                self.inventory.open_invent = False
                            elif self.inventory.open_invent == False:
                                self.inventory.open_invent = True
                        elif event.key == pygame.K_ESCAPE and self.inventory.open_invent == True:
                            self.menu.is_playing = False
                            self.music.music_play()

                clock.tick(60)

            else:
                self.menu.get_menu(self.screen, self.inventory.open_invent)
                self.menu.move_arrow()
                self.menu.play()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and self.menu.index_menu == 4:
                            self.sound.sound_play('click')
                            running = False
                        elif event.key == pygame.K_RETURN and self.menu.index_menu == 3:
                            if self.menu.panda_print == True:
                                self.menu.panda_print = False
                            elif self.menu.panda_print == False:
                                self.sound.sound_play('pikachu', volume=0.5)
                                self.menu.panda_print = True



        pygame.quit()




