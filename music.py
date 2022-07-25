import pygame
from dataclasses import dataclass


class Music:

    def __init__(self):
        # Initialisation du module
        pygame.mixer.init()
        self.music = {
            'house_player1': 'assets/music/sweetchildomine.mp3',
            'house_player2': 'assets/music/sweetchildomine.mp3',
            'ça': 'assets/music/rasputin.mp3',
            'menu': 'assets/music/heartofgold.mp3',
            'world': 'assets/music/heartofgold.mp3',
            'surmoi': 'assets/music/jumpinjackflash.mp3',
            'dungeon': 'assets/music/aceofspade.mp3'
        }

        # Exceptions (de pas relancer le même morceau mais le laisser continuer)
        # Pour l'origine à gauche, la cible à droite est invalidée (ne change par la musique)
        # 1 exception possible par monde d'origine
        self.music_exceptions = {
            'house_player1' : 'house_player2',
            'house_player2' : 'house_player1'
        }


    def music_play(self, origin_world = 'none', target_world = 'menu', volume=0.2):
        morceau = self.music[target_world]

        # Condition pour définir des exceptions (pour ne pas relancer le même morceau)
        if origin_world not in self.music_exceptions:
            pygame.mixer.music.load(morceau)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(volume)
        elif self.music_exceptions[origin_world] != target_world:
            pygame.mixer.music.load(morceau)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(volume)



