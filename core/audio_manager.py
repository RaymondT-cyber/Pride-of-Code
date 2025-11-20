import pygame, os

class AudioManager:
    def __init__(self):
        # Try to initialize audio, but don't fail if unavailable (headless)
        self.audio_available = False
        try:
            pygame.mixer.init()
            self.audio_available = True
        except Exception as e:
            print(f"Audio not available: {e}")
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
