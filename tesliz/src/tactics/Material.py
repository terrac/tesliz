from tactics.Singleton import *
import ogre.renderer.OGRE as ogre
import ogre.physics.OgreNewt as OgreNewt
from utilities.physics import *
s = Singleton()


class Material(object):
    def __init__(self,name,objectcallback):
        
        if s.app.materialmap.has_key(name):
            return s.app.materialmap[name]
        World = s.app.World
        sceneManager = s.app.sceneManager
        self.MatDefault = World.getDefaultMaterialID()
        self.MatObject = OgreNewt.MaterialID( World )
        self.MatPairDefaultObject = OgreNewt.MaterialPair( World, self.MatDefault, self.MatObject )
        self.ObjectCallback = objectcallback
        self.MatPairDefaultObject.setContactCallback( objectcallback )
        self.MatPairDefaultObject.setDefaultFriction( 1.5, 1.4 )
        s.app.materialmap[name] = self