def setStart(obj,unit1,unit2=None,position=None):  
    

        

    
    if unit1:
        obj.unit1 = unit1
        try:
            obj.choiceStart()
        except:
            pass        
    if unit2:
        obj.unit2 = unit2
            
    if unit2:
        obj.endPos = unit2.node.getPosition()
        
    if position:            
        obj.endPos = position
    try:
        if obj.endPos:        
            obj.choiceEnd()
    except:
        pass    
        
    try :
        return obj.ready()
    except:
        pass
    try :
        dis = distance(self.endPos, self.unit1.body.getOgreNode().getPosition())
        if dis > self.range:
            return False
    except:
        pass
    return True