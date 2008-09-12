from data.traits.generictraits import *
from tactics.util import *
#import data.traits.Generictraits as GT
from userinterface.Numberedtraits import *

from tactics.Move import *
from tactics.Attack import *
#from data.traits.GenericTrait import Move

from tactics.Singleton import *
import ogre.renderer.OGRE as ogre
import ogre.physics.OgreNewt as OgreNewt
from utilities.physics import *
s = Singleton()
class Unittypes(object):
    def FastFighter(self,unit,level):
        unit.node.getAttachedObject(0).setMaterialName("Examples/RustySteel")
        unit.attributes.speed = 4
        unit.attributes.hitpoints = 50* level        
        unit.attributes.damage = 50*level
        move = NumberedTraits([Move()],[5])
        unit.traits["Move"] = move
        attack = NumberedTraits([Attack()],[5])
        unit.traits["Attack"] = attack
        #range = NumberedTraits([JumpAttack()],[5])
        #unit.traits["JumpAttack"] = range               
#    def SlowFighter(self,unit):
#        unit.attributes.speed = 5
#        unit.attributes.hitpoints = 50        
#        unit.attributes.damage = 50
        
    def Mage(self,unit,level):
        unit.node.getAttachedObject(0).setMaterialName("Examples/RustySteel")
        unit.attributes.speed = 3
        #dir(self)
        #dir(data)
        #dir(GT)
        move = NumberedTraits([Move()],[5])
        unit.traits["Move"] = move
        attack = NumberedTraits([Attack()],[5])
        unit.traits["Attack"] = attack
        
        range = NumberedTraits([RangeAttack()],[5])
        unit.traits["BlackMagic"] = range
        
        unit.attributes.hitpoints = 50* level        
        unit.attributes.damage = 50* level

        