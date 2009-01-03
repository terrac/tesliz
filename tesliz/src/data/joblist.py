import data.traits.generictraits   
from data.actionlist import * 
from data.items import *
from userinterface.traits import *
from mental.mind import Mind
import mental.action
import copy
import data.jobs
import tactics.Affect

def set(unit,hp,power,mp,mpower,ce,speed,move):
    po =unit.attributes.magical = data.Stats.Stats()
    po.power = mpower
    po.points = mp
    po =unit.attributes.physical = data.Stats.Stats()
    
    po.maxpoints = hp
    po.points = hp
    po.power = power
    po.classevade = ce
    unit.attributes.speed = speed
    unit.attributes.moves = move
def setupJobList(unit):
    
    #nit.jobslist = []
    unit.joblist.append(Squire())
    unit.joblist.append(Chemist())
    if unit.job.required:
        unit.joblist + unit.job.required
    unit.joblist.append(unit.job)
      

    

class Squire(data.jobs.Job):
    
    def getAbilities(self):
        throw = Throw("cylinder.mesh",data.damage.halfBasicPhysical)
        abil = data.traits.basictraits.GridTargeting(data.traits.basictraits.GridTargeting.offset1,[throw],"Stone","physical",(5,5),4)
        
        
        #throw.do = lambda self,unit2: damageHitpoints(data.damage.test,self.unit1,unit2)
        
        trait1 =Traits([abil])
        
                #primary,reaction,support,movement
        return trait1
    def getMovement(self):
        list = [] 
        
        list.append(ClassAffect("moves","Move +1",MoveAdder(1,0)))
        
        return list
    def getLearnedOnStart(self):
        return ["Stone","Move +1"]
       
    def setupStats(self,unit):
        set(unit,30,4,5,3,5,6,(4,4))
    
class Chemist(data.jobs.Job):
    
    acquired = True
    def healing(self,abil):
        return abil.type == "healing"

    def setupStats(self,unit):
        set(unit,28,3,7,4,5,5,(3,3))
    def getAbilities(self):
        abil = data.traits.basictraits.GridTargeting(data.traits.basictraits.GridTargeting.offset1,[Throw(Potion())],"Potion","healing",)
        abil.range = 5,5
        abil.jobpoints = 50
        trait1 = ItemTraits([abil])
        
#        unit.traits["Chemist"] =ItemTraits([trait1],unit.player)
#        unit.mental = Mind([Combat(unit,self.healing,Combat.isWantedHurt),Combat(unit,Action.Attack,Combat.isWanted)])
        return trait1
    def getLearnedOnStart(self):
        return ["Potion"]
class Wizard(data.jobs.Job):
    
    def setupStats(self,unit):        
        set(unit,27,3,25,6,9,5,(3,3))
    def getAbilities(self):
        fireball = data.traits.basictraits.GridTargeting(data.traits.basictraits.GridTargeting.offset2,[Particle("RedTorch",sound="fireball.ogg"),DamageMagic(damage.basicMagical,"fire")],"Fireburst","fire",(5,5),20)
        
        #fireball.unittargeting = False
        trait1 = NumberedTraits([fireball],[50])
        fireball.learned = True
        return trait1
    def getLearnedOnStart(self):
        return ["Fireburst"]
    required = [("Chemist",2)]
    
class Knight(data.jobs.Job):
    
    def setupStats(self,unit):        
        set(unit,40,7,5,2,5,6,(4,4))
    def getAbilities(self):
        
        
        #fireball.unittargeting = False 
        trait1 = NumberedTraits([],[])
        
        return trait1
#    def getLearnedOnStart(self):
#        return ["Fireburst"]
    required = [("Squire",3)]
class Poet(data.jobs.Job):
    def setupStats(self,unit):        
        set(unit,25,5,25,5,5,7,(5,5))
   
    def getAbilities(self):
        deadzone = data.traits.basictraits.GridTargeting(data.traits.basictraits.GridTargeting.offset2,[Particle("RedTorch",sound="fireball.ogg"),AffectLand("deadzone")],"Deadzone")
        deadzone.range = 5,5
        trait1 = Traits([deadzone])
         
        return trait1
    def getLearnedOnStart(self):
        return ["Deadzone"]        
    required = [("Chemist",2)]
               
alljobs =[ Squire(),Chemist(),Wizard()]
