import data.util 
def setStart(ability,unit1,unit2=None,position=None):  
    

        

    
    if unit1:
        ability.unit1 = unit1
        
        if hasattr(ability, "choiceStart"):
            ability.choiceStart()
              
    if unit2:
        ability.unit2 = unit2
            
    if unit2:
        ability.endPos = unit2.node.getPosition()
        
    if position:            
        ability.endPos = position
    if hasattr(ability, "endPos"):
        if ability.endPos and hasattr(ability, "choiceEnd"):        
            ability.choiceEnd()
    
        
    if hasattr(ability, "ready"):
        return ability.ready()
    
    
    if hasattr(ability, "unit1") and hasattr(ability, "endPos") and not data.util.withinRange(ability.endPos, ability.unit1.body.getOgreNode().getPosition(),ability.range):
        return False

    if hasattr(ability, "needsasecondunit"):
        if ability.needsasecondunit:
            if not( hasattr(ability, "unit2") and  ability.unit2):
                return False
 
        
    return True