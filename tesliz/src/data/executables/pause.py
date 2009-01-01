
class Pause:
    def __init__(self,time):
        self.time = time
        self.unit1 = self
        
    def execute(self,timer):
        return False
        #self.time -= timer
        #print self.time
        #if self.time < 0:
        #    return False
        #return True
    