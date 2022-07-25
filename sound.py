import pygame


class SoundManager:

    def __init__(self):
        # Initialisation du module
        pygame.mixer.init()

        # List des sons
        self.sounds = {
            'click': pygame.mixer.Sound('assets/sounds/click.ogg'),
            'gameover': pygame.mixer.Sound('assets/sounds/game_over.ogg'),
            'tir': pygame.mixer.Sound('assets/sounds/tir.ogg'),
            'meteorite': pygame.mixer.Sound('assets/sounds/meteorite.ogg'),
            'pikachu' : pygame.mixer.Sound('assets/sounds/pikachu.ogg')
        }


    def sound_play(self, name, volume = 1):
        self.sounds[name].set_volume(volume)
        self.sounds[name].play()
