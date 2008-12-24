from tactics.Singleton import *
import random


class Queue:
    unitmap = dict()
    def getUnitList(self):
        return self.unitmap.keys()
    def addToQueue(self, unit,action):
        
        action.running = True
        
        if not hasattr(unit, "timeleft"):
            unit.timeleft = 0
        if not self.unitmap.has_key(unit):
            self.unitmap[unit] = [] 
        self.unitmap[unit].append(action)
#        if not unit in self.unitqueues:
#            self.unitqueues.append(unit)

         
 #   unitqueues = []   
    def getActiveQueue(self):
        return len(self.unitmap)

    def clearActions(self,unit):
        #dir([])
        del self.unitmap[unit]
    def clearUnitQueue(self):
        self.unitmap = dict()
            
    def isActive(self,unit):
        
        if self.unitmap.has_key(unit):
            return True
        
                  
        return False
    a =       0
    def runQueue(self,timer):
        
        self.a += timer
        for unit in self.unitmap.keys():
            
            
            if unit.timeleft > 0:
                unit.timeleft -= timer
                continue
           
            
            if len(self.unitmap[unit]) == 0:
                del self.unitmap[unit]
                continue
            iexecute = self.unitmap[unit][0]
            boo = False
           
            boo = iexecute.execute(timer)
            
            if not boo and len(self.unitmap[unit]):
                if hasattr(unit, "name"):
                    name = unit.name
                else:
                    name = str(unit)
                s.log("executable done "+ name+" "+str(iexecute),self)
                self.unitmap[unit].pop(0)
                if hasattr(iexecute, "timeleft"):
                    
                    unit.timeleft = iexecute.timeleft
                    unit.timeleft += random.random()*.1
                    
               
                
                    
                    
                
            
#            if s.turnbased :   
#                break    
