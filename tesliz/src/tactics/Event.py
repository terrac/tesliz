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
    def __init__(self, positionmap = dict(), turnmap = dict(),startlist = []):
        self.positionmap = positionmap
        self.turnmap = turnmap
        self.startlist = startlist
        for x in turnmap.values():
            for y in x.keys():
                x[y] = ScriptEvent(x[y])
#        slist = []
#        for x in self.startlist:
#            slist.append(ScriptEvent(x))
        self.startlist = ScriptEvent(self.startlist)
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
            s.framelistener.pauseturns = True
            s.framelistener.unitqueue.addToQueue(unit,exe)
            #s.framelistener.backgroundqueue.addToQueue(unit,UnpauseTurnsOnEnd())
            
    def start(self,test = False):
        oldspeed = 0
        if test:
            oldspeed = s.speed
            s.speed = 50
        
        unit = Unit()
        s.framelistener.pauseturns = True
        #for exe in self.startlist:
       
        s.framelistener.unitqueue.addToQueue(unit,self.startlist)
        unpause = UnpauseTurnsOnEnd(oldspeed)
        s.framelistener.unitqueue.addToQueue(unpause,unpause)
        
        
    def end(self):
        for unit in s.unitmap.values():            
            if self.turnmap.has_key(unit) and self.turnmap[unit].has_key("end"):
                exe = self.turnmap[unit]["end"]
                
                s.framelistener.unitqueue.addToQueue(unit,exe)
                
    
    def death(self,unit):
        dkey = "death-"+unit.getName()
        if self.turnmap.has_key(unit) and self.turnmap[unit].has_key(dkey):
            exe = self.turnmap[unit][dkey]
            unit, blah = exe.tlist[0]
            s.framelistener.unitqueue.addToQueue(unit,exe)