\
#from data.actionlist import * 
#from data.items import *
import userinterface.traits 
import mental.combat 
import mental.mind
#from mental.mind import Mind
import mental.action
import copy
import data.Stats



#class JobHolder:
#    def __init__(self):
#        self.job = None
#        self.jlist = []
#        
#    def setJob(self,value):
#        self.job = job

requiredexp =[0,200,400,700,1100,1600,2000,2500]


jobabilitymap = dict()

choosablemap ={"Reaction":dict(),"Movement":dict(),"Support":dict()}    
    

class Job(object):
    level = 1
    exp = 60
    
    def __init__(self,level = 1):
        self.level = level
        #map of reaction, trait1, trait2, etc
        self.traits = dict()
        self.learnedabilitynames = []
        if not jobabilitymap.has_key(self.getName()):
            jobabilitymap[self.getName()]=self.getAbilities()
            jobabilitymap[self.getName()].name = self.getName()
            #jobreactionmap[self.getName()]=self.getReactionAbilities()
            
            for x in choosablemap.keys():
                if hasattr(self, "get"+x):
                    #map = getattr(jobs, ")
                    map = choosablemap[x]
                    if not map.has_key(self.getName()):
                        map[self.getName()] = getattr(self,"get"+x)()
                        
                        #automatically sets the types
                        for y in map[self.getName()]:
                            y.type = x
                #map[self.getName()].name = x
    def getName(self):
        return self.__class__.__name__
 
        

#    def setupStats(self,unit):
#        pass
#    def getTraits(self):
#        pass
    def changeTo(self,unit):
        self.setupStats(unit)        
        unit.traits.Primary = self.getTraits(unit)
        unit.mental = self.getMental(unit)
        unit.job = self
        #else:
            
        #unit.traits[self.getName()] =traits
    
    
        
    
    def getTraits(self,unit):
        
        trait =jobabilitymap[self.getName()]
        if hasattr(self, "getLearnedOnStart") and not len(self.learnedabilitynames):
            self.learnedabilitynames =self.learnedabilitynames +self.getLearnedOnStart()
        return trait.getLearned(self.learnedabilitynames,unit)
        #then need to specifically save the rest seperately because they are chosen
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
    def getMental(self,unit):
        return  mental.mind.Mind([mental.combat.Combat(unit,mental.action.Attack,mental.combat.isWanted)])
            
    mesh = "zombie.mesh"
    material = "DarkGrey/SOLID"
    def __str__( self ):
        return self.__class__.__name__

    
