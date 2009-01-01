from tactics.Singleton import *
import pygame.mixer
class PlaySound:
    def __init__(self,soundname):
        self.soundname = soundname
        
    def execute(self,timer):
        s.playsound(self.soundname,"")
        return
#class Pause:
#    def __init__(self,time):
#        self.time = time
#        self.unit1 = self
#        
#    def execute(self,timer):
#        return False
#        #self.time -= timer
#        #print self.time
#        #if self.time < 0:
#        #    return False
#        #return True
        