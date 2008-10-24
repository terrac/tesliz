import random
import math
def damageHitpoints(unit1,number,type = None,unit2=None):
    #determine resistance
#    if unit1.attributes.resistance.has_key(type):
#        number = (1-unit1.attributes.resistance[type]) * number
    
    
    dir1 = unit1.getDirection()
    dir2 = unit2.getDirection()
    
        
    #determine chance to hit
    if type == "physical":
        
        
        if random.randint(0,100) < unit1.attributes.physical.tohit: #blindness would have a low to hit for example
            unit2.animate("missed")
            return False 
    #    if both pointing in same direction then 100% as one is behind the other
        if dir1 == dir2:
            if random.randint(0,100) < unit1.attributes.physical.accessoryevade: #missed
                unit2.animate("missed")
                return False
        # if both are absolutely pointing the the same direction then they are facing each other
        elif math.fabs(dir1.x) == math.fabs(dir2.x) or math.fabs(dir1.z) == math.fabs(dir2.z):
            if random.randint(0,100) < unit1.attributes.physical.classevade: #missed
                unit2.animate("missed")
                return False  
            if random.randint(0,100) < unit1.attributes.physical.shieldevade: #missed
                unit2.animate("blocked")
                return False
            if random.randint(0,100) < unit1.attributes.physical.accessoryevade: #missed
                unit2.animate("missed")
                return False
        else: #on the side
            if random.randint(0,100) < unit1.attributes.physical.shieldevade: #missed
                unit2.animate("blocked")
                return False
            if random.randint(0,100) < unit1.attributes.physical.accessoryevade: #missed
                unit2.animate("missed")
                return False
            
        brav1 = unit1.attributes.bravery
        brav2 = unit2.attributes.bravery    
        #a higher bravery than opponent adds damage
        number += ((brav1 - brav2) / 100) * number 
    else: #magical
        if random.randint(0,100) < unit1.attributes.magical.classevade: #missed
            unit2.animate("missed")
            return False  
        if random.randint(0,100) < unit1.attributes.magical.shieldevade: #missed
            unit2.animate("blocked")
            return False
        if random.randint(0,100) < unit1.attributes.magical.accessoryevade: #missed
            unit2.animate("missed")
            return False
        faith1 = unit1.attributes.faith
        faith2 = unit2.attributes.faith    
        #high faith adds damage, but opponents lower faith reduces total damage so a faith of 0 cannot recieve magical damage or healing
        number += ((faith1  / 100) * number) * (faith2  / 100) 
    rand =random.randint(0,100)    
    
    #    if they are s
    
    unit1.attributes.hitpoints = unit1.attributes.hitpoints - number 
    
    s.log(str(unit2)+" damages "+str(unit1)+" for "+ str(number)+"with type:"+type+" :")
    #s.app.bodies.index(unit1.body)
    if unit1.attributes.hitpoints < 1:
        s.removeUnit(unit1)
        print unit1
    return True

#def getChanceToHit(type):
    
#def getDamage(number,type):