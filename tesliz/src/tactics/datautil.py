import data.util 
def setStart(obj,unit1,unit2=None,position=None):  
    

        

    
    if unit1:
        obj.unit1 = unit1
        
        try:
            obj.choiceStart()
        except AttributeError, e:
            print e        
    if unit2:
        obj.unit2 = unit2
            
    if unit2:
        obj.endPos = unit2.node.getPosition()
        
    if position:            
        obj.endPos = position
    try:
        if obj.endPos:        
            obj.choiceEnd()
    except AttributeError, e:
        print e            
        
    try :
        return obj.ready()
    except:
        pass
    try :
        if data.util.withinRange(self.endPos, self.unit1.body.getOgreNode().getPosition(),self.range):
            return False

    except:
        pass
    try:
        if obj.needsasecondunit:
            if not( hasattr(obj, "unit2") and  obj.unit2):
                return False
    except AttributeError, e:
        pass
        
    return True