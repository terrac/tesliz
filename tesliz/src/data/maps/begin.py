from tactics.util import *
from mental.mind import *
from mental.background import *
from tactics.Event import *
from tactics.createunits import *

class Unitdata(object):

    def floormap(self,unit):
        unit.node.getAttachedObject(0).setMaterialName( "LightBlue/SOLID" )
        #unit.node.setScale(Ogre.Vector3(5,5,5))
        
        buildImmoblePhysics(unit)  
  
    def setupEvents(self):
        pass