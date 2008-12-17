import data.traits.generictraits  
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




def setupJobList(unit):
    #nit.jobslist = []
    unit.joblist.append(Squire())
    unit.joblist.append(Chemist())
    if unit.job.required:
        unit.joblist + unit.job.required
    unit.joblist.append(unit.job)
      



#class JobHolder:
#    def __init__(self):
#        self.job = None
#        self.jlist = []
#        
#    def setJob(self,value):
#        self.job = job
def set(unit,hp,power,mp,mpower,ce,speed,move):
    po =unit.attributes.magical = Fstats()
    po.power = mpower
    po.points = mp
    po =unit.attributes.physical = Fstats()
    
    po.maxpoints = hp
    po.points = hp
    po.power = power
    po.classevade = ce
    unit.attributes.speed = speed
    unit.attributes.move = move
requiredexp =[0,200,400,700,1100,1600,2000,2500]


class Job(object):
    level = 1
    exp = 0
    
    def __init__(self,level = 1):
        self.level = level


    def getName(self):
        return self.__class__.__name__
 
        

#    def setupStats(self,unit):
#        pass
#    def getTraits(self):
#        pass
    def changeTo(self,unit):
        self.setupStats(unit)
        traits,reaction,support,abilities = self.getAbilities()
        unit.traits[self.getName()] =traits
            
                                         
    def addExp(self,unit,toadd):
        self.exp += toadd
        if requiredexp[self.level] < self.exp:
            self.level +=1
            self.addNewJobs(unit.joblist)
    required = None
    def addNewJobs(self,joblist):
        for ajob in alljobs:
            if ajob.required:                
                for job in ajob.required:
                    boo = False
                    
                    #if x meets requirements then check to see if it needs to be added
                    for x in joblist:
                        
                        if isinstance(x,job.__class__) and job.level <= x.level:
                            boo = True
                    if boo:
                        
                        #check to see if unit already has job
                        for x in joblist:
                            if isinstance(x,ajob.__class__):
                                boo = False
                        #if job not in list and meets requirement then add        
                        if boo:
                            joblist.append(copy.deepcopy(ajob))
            
    mesh = "zombie.mesh"
    material = "DarkGrey/SOLID"
    def __str__( self ):
        return self.__class__.__name__

    
class Squire(Job):
    
    def getAbilities(self):
        throw = Throw("cylinder.mesh")
        abil = data.traits.generictraits.GridTargeting(data.traits.generictraits.GridTargeting.offset1,[throw],"Stone","physical",)
        
        throw.do = lambda self,unit2: data.util.damageHitpoints(data.damage.basicPhysical,self.unit1,unit2)
        #throw.do = lambda self,unit2: damageHitpoints(data.damage.test,self.unit1,unit2)
        abil.range = 5
        trait1 =Traits([abil])
        abil.learned = True
                #primary,reaction,support,movement
        return (trait1,None,None,None)
       
    def setupStats(self,unit):
        set(unit,30,4,5,3,5,6,(4,4))
    
class Chemist(Job):
    
    acquired = True
    def healing(self,abil):
        return abil.type == "healing"

    def setupStats(self,unit):
        set(unit,28,3,7,4,5,5,(3,3))
    def getAbilities(self):
        abil = data.traits.generictraits.GridTargeting(data.traits.generictraits.GridTargeting.offset1,[Throw(Potion())],"Potion","healing",)
        abil.range = 50
        trait1 = ItemTraits([abil],unit.player)
        abil.learned = True
#        unit.traits["Chemist"] =ItemTraits([trait1],unit.player)
#        unit.mental = Mind([Combat(unit,self.healing,Combat.isWantedHurt),Combat(unit,Action.Attack,Combat.isWanted)])
        return (trait1,None,None,None)
class Wizard(Job):
    
    def setupStats(self,unit):        
        set(unit,27,3,25,6,9,5,(3,3))
    def getAbilities(self):
        fireball = data.traits.generictraits.GridTargeting(data.traits.generictraits.GridTargeting.offset2,[Particle("RedTorch"),DamageMagic(damage.basicMagical,"fire")],"Fireburst")
        fireball.range = 5
        trait1 = NumberedTraits([fireball],[50])
        abil.learned = True
        return (trait1,None,None,None)

    required = [Chemist(2)]
class Poet(Job):
    
    def changeTo(self,unit):
        set(unit,27,3,25,6,5,7,(3,3))

        deadzone = data.traits.generictraits.GridTargeting(data.traits.generictraits.GridTargeting.offset2,[Particle("RedTorch"),AffectLand("deadzone")],"Deadzone")
        deadzone.range = 50,50
        trait1 = NumberedTraits([deadzone],[5])
        return (trait1,None,None,None)
        
    required = [Chemist(2)]
def changeTo(unit,job):
    # No clue what jlist is, removing the call
    #if job.requiredJobs(unit.job.jlist):
        
    unit.job =  job
    
    job.changeTo(unit)
               
alljobs =[ Squire(),Chemist(),Wizard(),Poet()]