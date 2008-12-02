from utilities.physics import *
from tactics.Singleton import *
import ogre.physics.OgreNewt as OgreNewt
from tactics.Unit import *
from tactics.util import *
import random

s = Singleton()

class ScriptEvent:
    def __init__(self,text,unit = None):
        if isinstance(text, list):
            self.tlist = text
        elif isinstance(text, str):
            self.tlist = [(unit,text)]
        else:#tuple
            self.tlist = [text]
        self.unit1 = unit
        self.time = 0
        
    def execute(self,timer):
        if not self.tlist:
            return
        if self.time > 0:
            self.time -= timer
            return True
        tuple = self.tlist.pop(0)
        
        #if not a tuple
        
        if not hasattr(tuple,'__len__'):
            if hasattr(tuple,'unit1') and tuple.unit1:
                s.framelistener.addToQueue(tuple.unit1,tuple)
            else:
                tuple.execute(0)
            return True
        if len(tuple) ==3:
            x,y,z = tuple
        else:
            x,y = tuple
            z = 4                 
        s.chatbox.add(y,x,z)
        self.time = z
        return True
class Event:
    #do the dict param here
    def __init__(self, positionmap = None, turnmap = None):
        self.positionmap = positionmap
        self.turnmap = turnmap
        for x in turnmap.values():
            for y in x.keys():
                x[y] = ScriptEvent(x[y])
                
        self.turncount = dict()
       
        

    def updateMove(self,pos):
        for x in self.positionmap.keys():
            #print distance(x,pos)
            if data.util.getDistance(x,pos) < 10:
                self.positionmap[x].execute()
                del self.positionmap[x]
    def turnStarted(self,unit):
        if not self.turnmap.has_key(unit):
            return
        if self.turncount.has_key(unit):
            self.turncount[unit] += 1
        else : 
            self.turncount[unit] = 0
             
        if self.turnmap[unit].has_key(self.turncount[unit]):
            exe = self.turnmap[unit][self.turncount[unit]]

            s.framelistener.addToQueue(unit,exe)
    def end(self):
        for unit in s.unitmap.values():            
            if self.turnmap.has_key(unit) and self.turnmap[unit].has_key("end"):
                exe = self.turnmap[unit]["end"]
    
                s.framelistener.addToQueue(unit,exe)
                
    def death(self,unit):
        dkey = "death-"+unit.getName()
        if self.turnmap.has_key(unit) and self.turnmap[unit].has_key(dkey):
            exe = self.turnmap[unit][dkey]
            unit, blah = exe.tlist[0]
            s.framelistener.addToQueue(unit,exe)