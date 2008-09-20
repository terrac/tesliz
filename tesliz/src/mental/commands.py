from tactics.Singleton import *
 
s = Singleton()

class SetPosition:
    def __init__(self,name,mental):
        self.name =name
        self.mental = mental
    
    def execute(self,timer):
        self.mental.pos = self.endPos
        s.framelistener.addToQueue(self.mental.unit,self.mental)
        return False