from tactics.Singleton import *
 
s = Singleton()
#name for human interface
class SetPosition:
    def __init__(self,name,mental):
        self.name =name
        self.mental = mental
        
    def execute(self,timer):
        self.mental.pos = self.endPos
        s.framelistener.addToQueue(self.mental.unit,self.mental)
        return False
    
    
class BroadcastMessage:
    def __init__(self,name,text,unit):
        self.name =name
        self.unit = unit
        self.text = text
        
    
    def clicked(self):
        s.grammar.broadcast(self.text,self.unit)
        s.chatbox.add(self.text,self.unit)
    
    def execute(self,timer):
        pass