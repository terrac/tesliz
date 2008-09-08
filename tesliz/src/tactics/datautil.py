def setStart(obj,unit1,unit2=None,position=None):  
    

        

    
    if unit1:
        obj.unit1 = unit1        
    if unit2:
        obj.unit2 = unit2    
    if unit2:
        obj.endPos = unit2.node.getPosition()
    if position:            
        obj.endPos = position
        
    try :
        return obj.ready()
    except:
        pass
    return True