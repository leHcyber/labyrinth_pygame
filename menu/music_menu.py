import pygame
import os
pygame.init()
pygame.mixer.init()

class MusicManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.current = None

    def play(self, path):
        if self.current == path:
            return

        self.current = path

        full_path = os.path.join(self.base_dir, path)

        pygame.mixer.music.stop()
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play(-1)

import pygame

class SoundManager:
    def __init__(self):
        self.sounds = {}

    def load_sounds(self):
        self.sounds["coin"] = pygame.mixer.Sound("assets/sounds/coin.wav")
        self.sounds["death"] = pygame.mixer.Sound("assets/sounds/death.wav")
        self.sounds["disapear"] = pygame.mixer.Sound("assets/sounds/disapear.wav")
        self.sounds["envole"] = pygame.mixer.Sound("assets/sounds/envole.wav")
        self.sounds["game_over"] = pygame.mixer.Sound("assets/sounds/game_over.wav")
        self.sounds["impact"] = pygame.mixer.Sound("assets/sounds/impact.wav")
        self.sounds["item_collect"] = pygame.mixer.Sound("assets/sounds/item_collect.wav")
        self.sounds["pause"] = pygame.mixer.Sound("assets/sounds/pause.wav")
        self.sounds["portal"] = pygame.mixer.Sound("assets/sounds/portal.wav")
        self.sounds["win"] = pygame.mixer.Sound("assets/sounds/win.wav")


    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def set_volume(self, name, volume):
        if name in self.sounds:
            self.sounds[name].set_volume(volume)