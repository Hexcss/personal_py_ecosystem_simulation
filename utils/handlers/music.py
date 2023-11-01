import random
import pygame

class MusicHandler:
    def __init__(self, soundtracks):
        self.soundtracks = soundtracks
        pygame.mixer.init()

    def play_music(self):
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        self.play_random_track()

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_random_track(self):
        track = random.choice(self.soundtracks)
        pygame.mixer.music.load("./resources/music/" + track)
        pygame.mixer.music.play()

    def play_sound_effect(self, sound_effect_path):
        sound_effect = pygame.mixer.Sound(sound_effect_path)
        sound_effect.play()
