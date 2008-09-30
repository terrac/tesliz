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
        range = NumberedTraits([ProjectileAttack()],[5])
        unit.traits["FireMagic"] = range        
        
    
    def Spark(self,unit,level):
        setupBasic(unit, level)
        setupStats(unit, level, 4, 400, 5,10,10)

   
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
        setupStats(unit, level, 4, 100, 50,5,3)
        unit.attributes.resistance = {"slash":.50,"bludgeon":.50,"pierce":.50}
        
    def ZaiSoldier(self,unit,level):
        setupBasic(unit, level)
        setupStats(unit, level, 5,450,15,10)
        unit.attributes.resistance = {"slash":.80,"bludgeon":.80,"pierce":.80}    
    
        
        
        
        
        

        