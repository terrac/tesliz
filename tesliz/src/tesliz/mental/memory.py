from tactics.Singleton import *
 
s = Singleton()

class Memory:
    def __init__(self):
        self.currentMemory = []
        
    def addItem(self,item):
        self.currentMemory.append(item)
        if len(self.currentMemory) > 10:
            self.currentMemory.pop()
            
 
    def removeItem(self,item):
        try:
            self.currentMemory.remove(item)
        except:
            return False
        return True