from data.traits.generictraits import GridTargeting 
from data.actionlist import *
from data.items import *
from userinterface.traits import *
import mental.combat as combat
import copy
class Fstats():
 
    def __init__(self):
        
        self.classevade = 0
        self.shieldevade = 0
        self.accessoryevade = 0
        self.power = 3
        self.belief = 50
        self.tohit = 100
        self.points = 5
        self.maxpoints = 5

 
      



class JobHolder:
    def __init__(self):
        self.job = None
        self.jlist = []
        
    def setJob(self,value):
        self.job = job

def set(unit,hp,power,mp,mpower,ce,speed,move):
    po =unit.attributes.magical = Fstats()
    po =unit.attributes.physical = Fstats()
    po.maxpoints = hp
    po.points = hp
    po.power = power
    po.classevade = ce
    unit.attributes.speed = speed
    unit.attributes.move = move
   
class Job:
    level = 1
    exp = 100
    
    def incrementLevel(self,cjobs):
        
        for job in getJobList():
            for x in cjobs:
                if isinstance(job, cjobs.getclass):
                    continue
            if requiredJobs(cjobs):
                cjobs.append(copy.deepcopy(job))
                
                
    def requiredJobs(self,cjobs):
        return True
class Squire(Job):
    
    def changeTo(self,unit):
        set(unit,30,4,5,3,5,6,(4,4))
        throw = Throw("cylinder.mesh")
        trait1 = GridTargeting(GridTargeting.offset1,[throw],"Stone","physical",)
        
        throw.do = lambda self,unit2: damageHitpoints(data.damage.basicPhysical,self.unit1,unit2)
        trait1.range = 50
        
        unit.traits["Squire"] =Traits([trait1])
    
class Chemist(Job):
    acquired = True
    def healing(self,abil):
        return abil.type == "healing"

    def changeTo(self,unit):
        set(unit,28,3,7,4,5,5,(3,3))

        trait1 = GridTargeting(GridTargeting.offset1,[Throw(Potion())],"Potion","healing",)
        trait1.range = 50
        unit.player.items.addItem("Potion")
        unit.traits["Chemist"] =ItemTraits([trait1],unit.player)
        unit.mental = Mind([Combat(unit,self.healing,combat.isWantedHurt),Combat(unit,action.Attack,combat.isWanted)])
class Wizard(Job):
    def changeTo(self,unit):
        set(unit,27,3,25,6,5,5,(3,3))

        fireball = GridTargeting(GridTargeting.offset2,[Particle("RedTorch"),DamageMagic(20,"fire")],"Fireburst")
        range = NumberedTraits([fireball],[5])
        unit.traits["BlackMagic"] = range
        
    def requiredJobs(self,cjobs):
        for job in cjobs:
            if isinstance(job, Chemist) and job.level > 1:
                return True
def getJobList():
    return [Squire(),Chemist(),Wizard()]