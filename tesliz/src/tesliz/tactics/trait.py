class Trait:
    def __init__(self):
        self.map = dict()
        self.actionDone = False
        
    def reset(self):
        self.actionDone = True
        #for x in unit.traits.values():            
            #x.used = False