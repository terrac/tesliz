import ogre.renderer.OGRE as Ogre
import os
import shelve
import data.util
import tactics.util
 
import time
import data.overviewtrade
from tactics.Singleton import *
from utilities.physics import *
import ogre.gui.CEGUI as CEGUI
from utilities.CEGUI_framework import *
import tactics.util

class Unitdata(object):

     
        
#    def floormap(self,unit):
#        unit.node.getAttachedObject(0).setMaterialName( "LightBlue/SOLID" )
        #unit.node.setScale(Ogre.Vector3(5,5,5))
        
#        buildImmoblePhysics(unit)  
    def setupEvents(self):
        
        s.app.msnCam.setPosition(Ogre.Vector3(11, 22, -10))
        #s.app.camera.lookAt(Ogre.Vector3(0, 5, 0))
        s.app.msnCam.setOrientation(Ogre.Quaternion(0.305629, -0.144145, 0.851248, 0.401475))
        #data.util.createMesh("Plane.mesh",Ogre.Vector3(0,5,0),10)
        s.overviewmap.raySceneQuery = s.app.sceneManager.createRayQuery(Ogre.Ray())
        node = data.util.createMesh("cylinder.mesh", Ogre.Vector3(0, 20, 0))
        light = s.app.sceneManager.createLight(s.app.getUniqueName())
        light.setType(Ogre.Light.LT_POINT)
        node.attachObject(light)
        #s.overviewmap.createLocations(s.overviewmap.root)
        s.overviewmap.unit = tactics.Unit.Unit()
        s.overviewmap.unit.node = data.util.createMesh("zombie.mesh", s.overviewmap.cpos.getVec() + Ogre.Vector3(0, 5, 0))
        tactics.util.buildPhysics(s.overviewmap.unit)
        s.overviewmap.map.clear()
        CEGUI.WindowManager.getSingleton().destroyWindow("chatbox")
        print "loading"
        s.overviewmap.createLocations(s.overviewmap.root)
        s.framelistener.pauseturns = True