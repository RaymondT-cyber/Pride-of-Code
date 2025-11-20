import pygame, os

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sfx = {}
        self.music_channel = None

    def load_sfx(self, key, path):
        if os.path.exists(path):
            self.sfx[key] = pygame.mixer.Sound(path)

    def play_sfx(self, key):
        s = self.sfx.get(key)
        if s:
            s.play()

    def play_music(self, path, loops=-1):
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loops=loops)

    def stop_music(self):
        pygame.mixer.music.stop()
