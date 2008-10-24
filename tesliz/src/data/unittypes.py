from data.traits.generictraits import *

#import data.traits.Generictraits as GT
from userinterface.Numberedtraits import *

from tactics.Move import *
#from data.traits.GenericTrait import Move
import copy
from tactics.Singleton import *
import ogre.renderer.OGRE as ogre
import ogre.physics.OgreNewt as OgreNewt
from utilities.physics import *
from data.actionlist import *
from data.items import *
import mental.combat as combat
s = Singleton()


def setupBasic(unit, level):
    #unit.node.getAttachedObject(0).setMaterialName("Examples/RustySteel")
    move = Traits([Move()])
    unit.traits["Move"] = move
    attack = Traits([Attack()])
    unit.traits["Attack"] = attack
    #unit.attributes.hitpoints = 500 * level
    #unit.attributes.damage = 50 * level

def setupStats(unit, level,speed = 5,hitpoints= 50,strength= 5,dexterity = 5,intelligence =5):
    unit.attributes.speed = speed
    unit.attributes.maxhitpoints =hitpoints * level 
    unit.attributes.hitpoints = hitpoints * level
    
    unit.attributes.strength = strength * level
    unit.attributes.dexterity = dexterity * level
    unit.attributes.intelligence = intelligence * level
    
        

class Unittypes(object):
    
    

    def FastFighter(self,unit,level):
        setupBasic(unit, level)
        setupStats(unit, level, 5, 50, 20)
        
        #range = NumberedTraits([JumpAttack()],[5])
        #unit.traits["JumpAttack"] = range               
#    def SlowFighter(self,unit):
#        unit.attributes.speed = 5
#        unit.attributes.hitpoints = 50        
#        unit.attributes.damage = 50
        
    def RedMage(self,unit,level):
        setupBasic(unit, level)
        
        setupStats(unit, level, 5, 30, 5,5,20)
        range = NumberedTraits([ProjectileAttack()],[5])
        unit.traits["FireMagic"] = range
        
    def BlueMage(self,unit,level):
        setupBasic(unit, level)
        
        setupStats(unit, level, 5, 30, 5,5,20)
        projectile = ProjectileAttack()
        projectile.name = "Waterball"
        projectile.type = "water"
        projectile.sound = "waterball.wav"
        projectile.particlename = 'BlueTorch'
        range = NumberedTraits([projectile],[5])
        unit.traits["WaterMagic"] = range        
        
    
    def Spark(self,unit,level):
        setupBasic(unit, level)
        setupStats(unit, level, 4, 50, 5,10,10)

   
        attack = Attack()
        attack.range = 20
        attack.name = "Pistol"
        attack.sound = "gun.wav"
        attack.getDamage = lambda : unit.attributes.dexterity +unit.attributes.intelligence/2
        
        cattack = copy.copy(attack)
        
        cattack.name = "Aimed Pistol"
        #make random
        cattack.getDamage = lambda : (unit.attributes.dexterity +unit.attributes.intelligence/2 -5)   
        cattack.type = "critical"
        
        
        pattack = ProjectileAttack()
        pattack.range = 10
        pattack.name = "Grenade"
        range = NumberedTraits([attack,cattack,pattack],[6,6,1])
        unit.traits["Technology"] = range
    
    def Robot(self,unit,level):
        setupBasic(unit, level)
        setupStats(unit, level, 4, 150, 50,5,3)
        unit.attributes.resistance = {"slash":.50,"bludgeon":.50,"pierce":.50}
        
    def ZaiSoldier(self,unit,level):
        setupBasic(unit, level)
        setupStats(unit, level, 5,100,15,10)
        unit.attributes.resistance = {"slash":.80,"bludgeon":.80,"pierce":.80}    
    
        
        
    def Ta(self,unit,level):
        setupBasic(unit, level)
        setupStats(unit, level, 5,100,15,10)
        unit.attributes.resistance = {"slash":.80,"bludgeon":.80,"pierce":.80}
        affect = Affects(StatAffect({"strength":5}),"music")
        boost1 = Boost(affect,"strup")        
        affect =  Affects(StatAffect({"dexterity":5}),"music")
        boost2 = Boost(affect,"dexup")
        trait = Traits([boost1,boost2])
        unit.traits["Boost"] = trait    
        
    def Wizard(self,unit,level):
        setupBasic(unit, level)
        
        setupStats(unit, level, 5, 30, 5,5,20)
        fireball = GridTargeting(GridTargeting.offset2,[Particle("RedTorch"),DamageMagic(20,"fire")],"Fireball")
        range = NumberedTraits([fireball],[5])
        unit.traits["FireMagic"] = range
        
    def Priest(self,unit,level):
        setupBasic(unit, level)
        
        setupStats(unit, level, 5, 30, 5,5,20)
        
        
        trait1 = GridTargeting(GridTargeting.offset1,[Particle("WhiteTorch"),DamageMagic(-20,"heal")],"Heal","healing")
        trait1.value = -10
        #add a damage reduction effect that adds a damage reduce of 10 to all for this
        #trait2 = GridTargeting(GridTargeting.offset2,[Particle("WhiteTorch"),Do(Affects(DamageAffect({"all":10}),"speed"))],"protect")
        range = NumberedTraits([trait1],[5,5])
        unit.traits["Priest"] = range
        
        unit.mental = Mind([Combat(unit,action.Healing,combat.isWantedHurt),Combat(unit,action.Attack,combat.isWanted)])
        
        #mental.state = {"angry":0,"happy":0}
        
        
    def TimeMage(self,unit,level):
        setupBasic(unit, level)
        
        setupStats(unit, level, 5, 30, 5,5,20)
        
        
        trait1 = GridTargeting(GridTargeting.offset2,[Particle("GreenTorch"),AffectOther(Affects(StatAffect({"speed":3}),"speed"))],"haste")
        trait2 = GridTargeting(GridTargeting.offset2,[Particle("GreenTorch"),AffectOther(Affects(StatAffect({"speed":-3}),"speed"))],"slow")
        range = NumberedTraits([trait1,trait2],[5,5])
        unit.traits["TimeMagic"] = range
        isBoosted = lambda unit2,unit1: unit2.affect.has("speed")
        haste = lambda abil: abil.type == "haste"
        unit.mental = Mind([Combat(unit,haste,isBoosted),Combat(unit,action.Attack,combat.isWanted)])
        
    def Ninja(self,unit,level):
        setupBasic(unit, level)
        
        setupStats(unit, level, 3, 40, 10,5,5)
                
        unit.traits["Attack"] = Traits([DoubleAttack()])
        
    def Knight(self,unit,level):
        setupBasic(unit, level)
        
        setupStats(unit, level, 4, 50, 10,5,5)
                
    def Squire(self,unit,level):
        setupBasic(unit, level)
        throw = Throw()
        trait1 = GridTargeting(GridTargeting.offset1,[throw],"Stone","physical",)
        throw.do = lambda self,unit2: unit2.damageHitpoints(1,"physical",self.unit1)
        trait1.range = 50
        
        unit.traits["Squire"] =Traits([trait1])
        setupStats(unit, level, 4, 35, 5,5,5)          
    
    def healing(self,abil):
        return abil.type == "healing"
    
    def Chemist(self,unit,level):
        setupBasic(unit, level)
        
        setupStats(unit, level, 5, 30, 5,5,5)
        trait1 = GridTargeting(GridTargeting.offset1,[Throw(Potion()),RemoveItem("Potion")],"Potion","healing",)
        trait1.range = 50
        unit.player.items.addItem("Potion")
        unit.traits["Chemist"] =Traits([trait1])
        unit.mental = Mind([Combat(unit,self.healing,combat.isWantedHurt),Combat(unit,action.Attack,combat.isWanted)])
    