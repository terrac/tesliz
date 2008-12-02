from data.traits.generictraits import GridTargeting 
from data.actionlist import *
from data.items import *
from userinterface.traits import *
import mental.combat as Combat
from mental.mind import Mind
import mental.action
import copy
class Fstats(object):
    points = 5
    def __init__(self):
        
        self.classevade = 0
        self.shieldevade = 0
        self.accessoryevade = 0
        self.power = 3
        self.belief = 50
        self.tohit = 100
        #self.points = 5
        self.maxpoints = 5

    def getPoints(self):
        return self.__points


    def setPoints(self, value):
        if self.maxpoints < value:
            value = self.maxpoints
        self.__points = value


    def delPoints(self):
        del self.__points
    points = property(getPoints, setPoints, delPoints, "Points's Docstring")




 
      



#class JobHolder:
#    def __init__(self):
#        self.job = None
#        self.jlist = []
#        
#    def setJob(self,value):
#        self.job = job
def set(unit,hp,power,mp,mpower,ce,speed,move):
    po =unit.attributes.magical = Fstats()
    po =unit.attributes.physical = Fstats()
    po.maxpoints = hp
    po.points = hp
    po.power = power
    po.classevade = ce
    unit.attributes.speed = speed
    unit.attributes.move = move
requiredexp =[0,200,400,700,1100,1600,2000,2500]
class Job:
    level = 1
    exp = 0
    def jobName(self):
        return self.__class__.__name__
    def incrementLevel(self,cjobs):
        
        for job in getJobList():
            for x in cjobs:
                if isinstance(job, cjobs.getclass):
                    continue
            if requiredJobs(cjobs):
                cjobs.append(copy.deepcopy(job))
                
    
    def upgradeLevel(self):
        if requiredexp[level] < exp:
            level +=1
    required = None
    def requiredJobs(self,cjobs):
        if self.required:                
            for job,level in required:
                boo = False
                for x in cjobs:
                    if x.__class__.__name__ == job and level >= x.level:
                        boo = True
                if not boo:
                    return False
        return True
    mesh = "zombie.mesh"
    material = "Examples/RustySteel"
    def __str__( self ):
        return self.__class__.__name__
class Squire(Job):
    
 
    
    def changeTo(self,unit):
        set(unit,30,4,5,3,5,6,(4,4))
        throw = Throw("cylinder.mesh")
        trait1 = GridTargeting(GridTargeting.offset1,[throw],"Stone","physical",)
        
        throw.do = lambda self,unit2: data.util.damageHitpoints(data.damage.basicPhysical,self.unit1,unit2)
        #throw.do = lambda self,unit2: damageHitpoints(data.damage.test,self.unit1,unit2)
        trait1.range = 50
        
        unit.traits["Squire"] =Traits([trait1])
#        unit.mental = Mind([Combat(unit,Action.Attack,Combat.isWanted)])
    
class Chemist(Job):
    
    acquired = True
    def healing(self,abil):
        return abil.type == "healing"

    def changeTo(self,unit):
        set(unit,28,3,7,4,5,5,(3,3))

        trait1 = GridTargeting(GridTargeting.offset1,[Throw(Potion())],"Potion","healing",)
        trait1.range = 50
        
#        unit.traits["Chemist"] =ItemTraits([trait1],unit.player)
#        unit.mental = Mind([Combat(unit,self.healing,Combat.isWantedHurt),Combat(unit,Action.Attack,Combat.isWanted)])
class Wizard(Job):
    
    def changeTo(self,unit):
        set(unit,27,3,25,6,5,5,(3,3))

        fireball = GridTargeting(GridTargeting.offset2,[Particle("RedTorch"),DamageMagic(20,"fire")],"Fireburst")
        fireball.range = 50
        range = NumberedTraits([fireball],[5])
        unit.traits["BlackMagic"] = range
        

    required = [("Chemist",2)]
class Poet(Job):
    
    def changeTo(self,unit):
        set(unit,27,3,25,6,5,5,(3,3))

        deadzone = GridTargeting(GridTargeting.offset2,[Particle("RedTorch"),DamageMagic(20,"fire")],"Fireburst")
        fireball.range = 50
        range = NumberedTraits([fireball],[5])
        unit.traits["BlackMagic"] = range
        
    def requiredJobs(self,cjobs):
        for job in cjobs:
            if isinstance(job, Chemist) and job.level > 1:
                return True
def changeTo(unit,job):
    # No clue what jlist is, removing the call
    #if job.requiredJobs(unit.job.jlist):
        
    unit.job =  job
    
    job.changeTo(unit)
               
def getJobList():
    return [Squire(),Chemist(),Wizard()]