from tactics.Singleton import *
import random
class Queue:
    def addToQueue(self, unit,action):
        
        action.running = True
        if not hasattr(unit, "actionqueue"):
            unit.actionqueue = []
        if not hasattr(unit, "timeleft"):
            unit.timeleft = 0
        unit.actionqueue.append(action)
        if not unit in self.unitqueues:
            self.unitqueues.append(unit)

         
    unitqueues = []   
    def getActiveQueue(self):
        return len(self.unitqueues)

    def clearActions(self,unit):
        #dir([])
        if unit in self.unitqueues :
            self.unitqueues.remove(unit)
        
        unit.actionqueue = []
    def clearUnitQueue(self):
        for x in self.unitqueues:
            self.clearActions(x)
            
    def isActive(self,unit):
        
        if len( unit.actionqueue):
            return True
        
                  
        return False
    a =       0
    def runQueue(self,timer):
        
        self.a += timer
        for unit in self.unitqueues:
            
            
            if unit.timeleft > 0:
                unit.timeleft -= timer
                continue
           
            
            if len(unit.actionqueue) == 0:
                self.unitqueues.remove(unit)
                continue
            iexecute = unit.actionqueue[0]
            boo = False
           
            boo = iexecute.execute(timer)
            
            if not boo and len(unit.actionqueue):
                if hasattr(unit, "name"):
                    name = unit.name
                else:
                    name = str(unit)
                s.log("executable done "+ name+" "+str(iexecute),self)
                unit.actionqueue.pop(0)
                if hasattr(iexecute, "timeleft"):
                    
                    unit.timeleft = iexecute.timeleft
                    unit.timeleft += random.random()*.1
                    
               
                
                    
                    
                
            
#            if s.turnbased :   
#                break    
