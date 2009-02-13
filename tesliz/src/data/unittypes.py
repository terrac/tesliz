#import data.traits.generictraits 

#from data.traits.generictraits import GridTargeting
#import data.traits.Generictraits as GT
from userinterface.traits import *

 
#from data.traits.GenericTrait import Move
import copy
from tactics.Singleton import *
import ogre.renderer.OGRE as Ogre
import ogre.physics.OgreNewt as OgreNewt
from utilities.physics import *
from data.actionlist import *
from data.items import *
import data.jobs
import damage
import data.joblist
s = Singleton()


 

    


def setupStats(unit, level,speed = 5,hitpoints= 50,strength= 5,dexterity = 5,intelligence =5):
    unit.attributes.speed = speed
    unit.attributes.physical.maxpoints =hitpoints * level 
    unit.attributes.physical.points = hitpoints * level
    
    unit.attributes.physical.power = strength * level
    #unit.attributes.dexterity = dexterity * level
    unit.attributes.magical.power = intelligence * level
    
        

class Unittypes(object):
    
    

#    def FastFighter(self,unit,level):
#        setupBasic(unit, level)
#        setupStats(unit, level, 5, 50, 20)
#        
#        #range = NumberedTraits([JumpAttack()],[5])
#        #unit.traits["JumpAttack"] = range               
##    def SlowFighter(self,unit):
##        unit.attributes.speed = 5
##        unit.attributes.hitpoints = 50        
##        unit.attributes.damage = 50
#        
#    def RedMage(self,unit,level):
#        setupBasic(unit, level)
#        
#        setupStats(unit, level, 5, 30, 5,5,20)
#        range = NumberedTraits([ProjectileAttack()],[5])
#        unit.traits["FireMagic"] = range
#        
#    def BlueMage(self,unit,level):
#        setupBasic(unit, level)
#        
#        setupStats(unit, level, 5, 30, 5,5,20)
#        projectile = ProjectileAttack()
#        projectile.name = "Waterball"
#        projectile.type = "water"
#        projectile.sound = "waterball.wav"
#        projectile.particlename = 'BlueTorch'
#        range = NumberedTraits([projectile],[5])
#        unit.traits["WaterMagic"] = range        
#        
#    
#    def Spark(self,unit,level):
#        setupBasic(unit, level)
#        setupStats(unit, level, 4, 50, 5,10,10)
#
#   
#        attack = Attack()
#        attack.range = 20
#        attack.name = "Pistol"
#        attack.sound = "gun.wav"
#        attack.getDamage = lambda : unit.attributes.dexterity +unit.attributes.intelligence/2
#        
#        cattack = copy.copy(attack)
#        
#        cattack.name = "Aimed Pistol"
#        #make random
#        cattack.getDamage = lambda : (unit.attributes.dexterity +unit.attributes.intelligence/2 -5)   
#        cattack.type = "critical"
#        
#        
#        pattack = ProjectileAttack()
#        pattack.range = 10
#        pattack.name = "Grenade"
#        range = NumberedTraits([attack,cattack,pattack],[6,6,1])
#        unit.traits["Technology"] = range
#    
#    def Robot(self,unit,level):
#        setupBasic(unit, level)
#        setupStats(unit, level, 4, 150, 50,5,3)
#        unit.attributes.resistance = {"slash":.50,"bludgeon":.50,"pierce":.50}
#        
#    def ZaiSoldier(self,unit,level):
#        setupBasic(unit, level)
#        setupStats(unit, level, 5,100,15,10)
#        unit.attributes.resistance = {"slash":.80,"bludgeon":.80,"pierce":.80}    
#    
#        
#        
#    def Ta(self,unit,level):
#        setupBasic(unit, level)
#        setupStats(unit, level, 5,100,15,10)
#        unit.attributes.resistance = {"slash":.80,"bludgeon":.80,"pierce":.80}
#        affect = Affects(StatAffect({"strength":5}),"music")
#        boost1 = Boost(affect,"strup")        
#        affect =  Affects(StatAffect({"dexterity":5}),"music")
#        boost2 = Boost(affect,"dexup")
#        trait = Traits([boost1,boost2])
#        unit.traits["Boost"] = trait    
#        
#
#    def Priest(self,unit,level):
#        setupBasic(unit, level)
#        
#        setupStats(unit, level, 5, 30, 5,5,20)
#        
#        
#        trait1 = GridTargeting(GridTargeting.offset1,[Particle("WhiteTorch"),DamageMagic(-20,"heal")],"Heal","healing")
#        trait1.value = -10
#        #add a damage reduction effect that adds a damage reduce of 10 to all for this
#        #trait2 = GridTargeting(GridTargeting.offset2,[Particle("WhiteTorch"),Do(Affects(DamageAffect({"all":10}),"speed"))],"protect")
#        range = NumberedTraits([trait1],[5,5])
#        unit.traits["Priest"] = range
#        
#        unit.mental = Mind([Combat(unit,action.Healing,combat.isWantedHurt),Combat(unit,action.Attack,combat.isWanted)])
#        
#        #mental.state = {"angry":0,"happy":0}
#        
        
    def TimeMage(self,unit,level):
        #setupBasic(unit, level)
        
        setupStats(unit, level, 5, 30, 5,5,20)
        
        
        trait1 = GridTargeting(GridTargeting.offset2,[Particle("GreenTorch"),AffectOther(Affects(StatAffect({"speed":3}),"speed"))],"haste")
        trait2 = GridTargeting(GridTargeting.offset2,[Particle("GreenTorch"),AffectOther(Affects(StatAffect({"speed":-3}),"speed"))],"slow")
        range = NumberedTraits([trait1,trait2],[5,5])
        unit.traits["TimeMagic"] = range
        isBoosted = lambda unit2,unit1: unit2.affect.has("speed")
        haste = lambda abil: abil.type == "haste"
        unit.mental = Mind([Combat(unit,haste,isBoosted),Combat(unit,action.Attack,combat.isWanted)])
        
    def Ninja(self,unit,level):
        #setupBasic(unit, level)
        
        setupStats(unit, level, 3, 40, 10,5,5)
                
        unit.traits["Attack"] = Traits([DoubleAttack()])
        
    def Knight(self,unit,level):
        #setupBasic(unit, level)
        
        unit.job = data.joblist.Knight()
        unit.items.add(PlateArmor())
        unit.items.add(Helm())
        unit.items.add(Knightsword())
    def Poet(self,unit,level):
        #setupBasic(unit, level)
        unit.job = data.joblist.Poet()
        unit.items.add(LeatherArmor())
        unit.items.add(ClothCap())
        unit.items.add(Broadsword())
    def Wizard(self,unit,level):
        #setupBasic(unit, level)
        unit.job = data.joblist.Wizard()
 
        
        unit.items.add(ClothCap())
        unit.items.add(Dagger())
        #fireball = data.traits.basictraits.GridTargeting(data.traits.generictraits.GridTargeting.offset2,[Particle("RedTorch"),DamageMagic(20,"fire")],"Fireball")
        #range = NumberedTraits([fireball],[5])
        #unit.traits["FireMagic"] = range
                        
    def Squire(self,unit,level):
        #setupBasic(unit, level)
        unit.job = data.joblist.Squire()
 
        unit.items.add(LeatherArmor())
        unit.items.add(ClothCap())
        unit.items.add(Broadsword())
 
            
    
    
    def Chemist(self,unit,level):
        #setupBasic(unit, level)
        unit.job = data.joblist.Chemist()
 
        unit.items.add(LeatherArmor())
        unit.items.add(ClothCap())
        unit.items.add(Broadsword())
#       manager.util.resetAttributes(unit)
        
           