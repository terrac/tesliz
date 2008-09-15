from data.traits.generictraits import *
from tactics.util import *
#import data.traits.Generictraits as GT
from userinterface.Numberedtraits import *

from tactics.Move import *
#from data.traits.GenericTrait import Move

from tactics.Singleton import *
import ogre.renderer.OGRE as ogre
import ogre.physics.OgreNewt as OgreNewt
from utilities.physics import *
s = Singleton()


def setupBasic(unit, level):
    unit.node.getAttachedObject(0).setMaterialName("Examples/RustySteel")
    move = Traits([Move()])
    unit.traits["Move"] = move
    attack = Traits([Attack()])
    unit.traits["Attack"] = attack
    unit.attributes.hitpoints = 50 * level
    unit.attributes.damage = 50 * level
    
class Unittypes(object):


    def FastFighter(self,unit,level):
        setupBasic(unit, level)
        unit.attributes.speed = 4
        #range = NumberedTraits([JumpAttack()],[5])
        #unit.traits["JumpAttack"] = range               
#    def SlowFighter(self,unit):
#        unit.attributes.speed = 5
#        unit.attributes.hitpoints = 50        
#        unit.attributes.damage = 50
        
    def Mage(self,unit,level):
        setupBasic(unit, level)
        
        unit.attributes.speed = 3
        range = NumberedTraits([ProjectileAttack()],[5])
        unit.traits["BlackMagic"] = range
        
    
    def Spark(self,unit,level):
        setupBasic(unit, level)
        
        unit.attributes.speed = 2
        attack = Attack()
        attack.range = 20
        attack.name = "Pistol"
        range = NumberedTraits([attack],[5])
        
        pattack = ProjectileAttack()
        pattack.range = 10
        pattack.name = "Grenade"
        range = NumberedTraits([attack,pattack],[6,1])
        unit.traits["Technology"] = range
    
    
        
        
    
        
        
        
        
        

        