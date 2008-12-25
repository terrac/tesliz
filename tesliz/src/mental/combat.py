from tactics.Singleton import *
import tactics.util
import utilities.physics
import data.util
import tactics.datautil
import copy
s = Singleton()



def isWantedHurt(eunit,unit):
    return eunit.player ==unit.player and eunit.attributes.physical.points < eunit.attributes.physical.maxpoints

def isWanted(eunit,unit):
    return eunit.player !=unit.player 




def getBestList(unit,isValid):
    bestl = []
    best = None
    traitlist = []
    for trait in unit.traits.getUsable():        
       if trait:
           for ability in trait.getAbilities().values():               
               if isValid(ability):
                   traitlist.append((ability.value,ability))
                   
    traitlist.sort()
    return traitlist

def getWithinRange(unit,eunit,isValid):
    best = None
    for trait in unit.traits.getUsable():
       if trait:
           for ability in trait.getClassList():
               if isValid(ability):
                   if not best:
                       best = ability                
                   elif best.value <ability.value and data.util.withinRange(eunit.body.getOgreNode().getPosition(), unit.body.getOgreNode().getPosition(), ability.range):
                       best = ability
                   
    return best


def getCloseList(unit,isWanted):

    
    lodis = 999
    lounit = None
    position = unit.node.getPosition()
    tuplelist = []
    for unit2 in s.unitmap.values():
        if isWanted(unit2,unit) and not unit2.getDeath() and unit2.node:
            tuple = utilities.physics.distance(unit2.node.getPosition(),position),unit2
            tuplelist.append(tuple)
    tuplelist.sort()
    
    return tuplelist

class Combat(object):
    
    
    def __init__(self,unit,isValid, isWanted,cautious = False):
        self.unit =unit
        self.isValid = isValid
        self.running = True
        #if getClose:
        self.isWanted = isWanted
#        else:
#            self.getClose combat.getClose
        self.state = "start"    
        self.wait = 0
        self.cautious = cautious
        

    def setupMove(self):
        unit = self.unit

        #s.framelistener.clearAction
        eunit = getClose(unit,self.isWanted)
        self.eunit = eunit
        if not self.eunit:                
            return False
        bool = False
        move = unit.traits["Move"].getClassList()[0]
        abill = getBest(unit, self.isValid)
        vlist = data.util.getAllValid(unit.body.getOgreNode().getPosition(), unit.attributes.moves)
        #vlist.reverse()
        endvec = None
        endabil = None
        self.validvecs = []
        while abill and not endvec:
            abil = abill.pop()
            validvecs = []
            for vec in vlist:
            #ray from vec to enemy unit, if valid then move there, but only
                start = vec
                end = eunit.body.getOgreNode().getPosition()
                # print start
                self.ray = OgreNewt.BasicRaycast(s.app.World, start, end)
                info = self.ray.getFirstHit()
                #print start
                #print end
                if info.mBody:
                    name = info.mBody.getOgreNode().getName()
                    if (s.unitmap.has_key(name) and s.unitmap[name].player != unit.player and data.util.withinRange(vec, end, abil.range)):
                        validvecs.append(vec)
                    #break;
                    
                
            
            lodis = 999
            for vec in validvecs:
                dis = utilities.physics.distance(eunit.node.getPosition(), vec)
                if dis < lodis:
                    lodis = dis
                    endvec = vec
                    endabil = abil
            self.validvecs = validvecs
                
            
            print lodis
        self.endabil = endabil
        self.endvec = endvec
        self.vlist = vlist
        self.move = move
        return True


    def chooseBest(self,unit):
        bestabilitieslist = getBestList(unit, self.isValid)
        unitlist = getClose(unit,self.isWanted)
        for ability in bestabilitieslist:
            for unit in unitlist:
                #test range
                xm, ym = unit.attributes.moves.range
                xa, ya = ability.range
                
                #might need to reverse
                ability.offset.sort()
                #add the x and y as the extension of the offset range
                xo,xa,notused = ability.offset[0]
                
                range = xm+xa+xo,ym+ya+yo
#                tactics.util.
                #find best offset and set
                position2 = unit2.node.getPosition()
                position1 = unit1.node.getPosition()
                if data.util.withinRange(position1,position2,range):
                    for offset in ability.offset:
                        #get from position2 to the place that would be chosen
                        tohit = position2 - offset
                        #calculate damage from this hit
                        for off in ability.offset:
                            unit =data.util.getValidUnit(tohit + offset, range[1])
                            if unit:
                                data.util.getChanceToHitAndDamage(number, type, unit1, unit2)
    
    def execute(self,timer):
        #aoeu
        if self.wait > 0:
            self.wait -= timer
            return True
        
        unit = self.unit
        if not unit.node:
            return False

        
        
        if self.state == "start": 
            if not self.setupMove():
                return False
            self.state = "showmoves"
        if self.state == "showmoves":
            self.nlist = []
            for vec in self.vlist:
                self.nlist.append(data.util.show(vec))
                
            self.wait = 2
            self.state ="showchoice"
            return True
        if self.state == "showchoice":  #show choices for now
            for x in self.nlist:                    
                s.app.sceneManager.getRootSceneNode().removeChild(x)
            self.nlist = []
            for vec in self.validvecs:
                self.nlist.append(data.util.show(vec,"BlueMage/SOLID"))
            if self.endvec:
                self.nlist.append(data.util.show(self.endvec + Ogre.Vector3(0,1,0),"RedMage/SOLID"))
            self.wait = 2
            self.state ="addactions"
            return True
        if self.state == "addactions":
            for x in self.nlist:                    
                s.app.sceneManager.getRootSceneNode().removeChild(x)
            if not self.endvec:
                self.endvec = self.eunit.body.getOgreNode().getPosition()
            tactics.datautil.setStart(self.move,unit,None,self.endvec)
            s.framelistener.unitqueue.addToQueue(unit,copy.copy(self.move))
            if self.endabil:
                tactics.datautil.setStart(self.endabil,unit,self.eunit)              
                s.framelistener.unitqueue.addToQueue(unit,copy.copy(self.endabil))
            self.state = "start"
            return False
        
        
        #unit.mental.state["angry"] = 50#     
        return True
    
