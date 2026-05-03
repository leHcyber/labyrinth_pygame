import os
import pygame

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Map:
    def __init__(self, level, global_images):
        self.level = level
        self.level_id = level.get("id", "unknown")

        self.textures = {}

        # 1. textures locales du level
        for key, path in level.get("textures", {}).items():
            self.textures[key] = pygame.image.load(
                os.path.join(BASE_DIR, path)
            ).convert_alpha()

        # 2. fallback sur images globales (important !)
        self.global_images = global_images

    def get_image(self, key):
        return self.textures.get(key) or self.global_images.get(key)