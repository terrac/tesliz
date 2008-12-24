class Timer:
    def __init__(self):
        
        self.count = 0
        self.dictcount = dict()
        
    def broadcast(self,text):
        if self.dictcount.has_key(self.count):
            self.dictcount[self.count].broadcast(text)
        self.count += 1
        

