from utilities.physics import *
from tactics.Singleton import *
import ogre.physics.OgreNewt as OgreNewt
from tactics.Unit import *
from tactics.util import *
from ogre.renderer.OGRE import Vector3
import random
import utilities.FollowCamera

s = Singleton()

class UnpauseTurnsOnEnd:
#    def __init__(self, bool):
#        self.bool = bool
    def __init__(self,oldspeed = None):
        self.oldspeed = oldspeed
    def execute(self,timer):
        
        if s.framelistener.unitqueue.getActiveQueue():
            for x in s.framelistener.unitqueue.getUnitList():
                if isinstance(x, UnpauseTurnsOnEnd):
                    continue
                if isinstance(x, utilities.FollowCamera.FollowCamera):
                    continue
                #not done
                return True
        if self.oldspeed:
            s.speed = self.oldspeed
        s.framelistener.pauseturns = False
        
        
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
        if self.time > 0:
            self.time -= timer
            return True
        if not self.tlist:

            
            return

        tuple = self.tlist.pop(0)
        
        #if not a tuple
        
        if not hasattr(tuple,'__len__'):
            if hasattr(tuple,'unit1') and tuple.unit1:
                
                #saved scripts will only have strings
                if isinstance(tuple.unit1, str):
                    tuple.unit1 = s.unitmap[tuple.unit1]
                if hasattr(tuple,'unit2') and tuple.unit1 and isinstance(tuple.unit1, str):
                    tuple.unit1 = s.unitmap[tuple.unit1]
                if hasattr(tuple, 'endPos') and isinstance(tuple.endPos, str): 
                    tuple.endPos = eval(tuple.endPos)
                    
                s.framelistener.unitqueue.addToQueue(tuple.unit1,tuple)
            else:
                tuple.execute(0)
            return True
        if len(tuple) ==3:
            x,y,z = tuple
        else:
            x,y = tuple
            z = 4       
        #saved scripts will only have strings
        if isinstance(x, str):
            x = s.unitmap[x]
        
                          
        s.chatbox.add(y,x,z)
        self.time = z
        return True
class Event:
    #do the dict param here
    def __init__(self, scriptmap):
        self.turn = None
        self.position = None
        self.start = None
        self.end = None
#        if scriptmap.has_key("position"):
#            self.position = scriptmap["position"]
#        if scriptmap.has_key("turn"):
#            self.turn = scriptmap["turn"]
#        if scriptmap.has_key("start"):
#            self.startlist = scriptmap["start"] 
        for x in scriptmap:
            setattr(self, x, scriptmap[x])
        if self.turn:
            for x in self.turn.values():
                for y in x.keys():
                    x[y] = ScriptEvent(x[y])
#        slist = []
#        for x in self.startlist:
#            slist.append(ScriptEvent(x))
        self.start = ScriptEvent(self.start)
        self.turncount = dict()
       
        

    def updateMove(self,pos):
        for x in self.position.keys():
            #print distance(x,pos)
            if data.util.getDistance(x,pos) < 10:
                self.position[x].execute()
                del self.position[x]
    def turnStarted(self,unit):
        if  not self.turn or not self.turn.has_key(unit):
            return
        if self.turncount.has_key(unit):
            self.turncount[unit] += 1
        else : 
            self.turncount[unit] = 0
             
        if self.turn[unit].has_key(self.turncount[unit]):
            exe = self.turn[unit][self.turncount[unit]]
            s.framelistener.pauseturns = True
            s.framelistener.unitqueue.addToQueue(unit,exe)
            #s.framelistener.backgroundqueue.addToQueue(unit,UnpauseTurnsOnEnd())
            
    def startEvent(self,test = False):
        oldspeed = 0
        if test:
            oldspeed = s.speed
            s.speed = 50
        
        if self.start:
            unit = Unit()
            s.framelistener.pauseturns = True
            #for exe in self.startlist:
             
            s.framelistener.unitqueue.addToQueue(unit,self.start)
            unpause = UnpauseTurnsOnEnd(oldspeed)
            s.framelistener.unitqueue.addToQueue(unpause,unpause)
        
        
    def endEvent(self):
        if self.end:
            unit = Unit()
            s.framelistener.pauseturns = True
            #for exe in self.startlist:
           
            s.framelistener.unitqueue.addToQueue(unit,self.end)
            unpause = UnpauseTurnsOnEnd()
            s.framelistener.unitqueue.addToQueue(unpause,unpause)
                    
    
    def death(self,unit):
        dkey = "death-"+unit.getName()
        if self.turn.has_key(unit) and self.turn[unit].has_key(dkey):
            exe = self.turn[unit][dkey]
            unit, blah = exe.tlist[0]
            s.framelistener.unitqueue.addToQueue(unit,exe)