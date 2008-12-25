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
        throw = Throw("cylinder.mesh")
        abil = data.traits.basictraits.GridTargeting(data.traits.basictraits.GridTargeting.offset1,[throw],"Stone","physical",)
        
        throw.do = lambda self,unit2: data.util.damageHitpoints(data.damage.halfBasicPhysical,self.unit1,unit2)
        #throw.do = lambda self,unit2: damageHitpoints(data.damage.test,self.unit1,unit2)
        abil.range = 5
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
        abil.range = 50
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
        fireball = data.traits.basictraits.GridTargeting(data.traits.basictraits.GridTargeting.offset2,[Particle("RedTorch"),DamageMagic(damage.basicMagical,"fire")],"Fireburst")
        fireball.range = 5
        fireball.value = 20
        trait1 = NumberedTraits([fireball],[50])
        fireball.learned = True
        return trait1
    def getLearnedOnStart(self):
        return ["Fireburst"]
    required = [("Chemist",2)]
class Poet(data.jobs.Job):
    
#    def changeTo(self,unit):
#        set(unit,27,3,25,6,5,7,(3,3))
#
#        deadzone = data.traits.basictraits.GridTargeting(data.traits.basictraits.GridTargeting.offset2,[Particle("RedTorch"),AffectLand("deadzone")],"Deadzone")
#        deadzone.range = 50,50
#        trait1 = NumberedTraits([deadzone],[5])
#        return trait1
    
    def getAbilities(self):
        pass
        
    required = [("Chemist",2)]
               
alljobs =[ Squire(),Chemist(),Wizard()]
