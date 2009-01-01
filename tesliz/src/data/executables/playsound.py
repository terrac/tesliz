from tactics.Singleton import *
import pygame.mixer
class PlaySound:
    def __init__(self,soundname):
        self.soundname = soundname
        
    def execute(self,timer):
        s.playsound(self.soundname,"")
        return
    