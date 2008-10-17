from tactics.Singleton import *
import ogre.renderer.OGRE as ogre
s = Singleton()

class Particle():
    def __init__(self, name):
        self.particlename = name
    def execute(self,unit1,unit,endpos):
    
        name = s.app.getUniqueName()
        
        node = s.app.sceneManager.getRootSceneNode().createChildSceneNode( name + "Node" )
        node.setPosition(Ogre.Vector3(endpos))
        psm = ogre.ParticleSystemManager.getSingleton()

        particleSystem2 = s.app.sceneManager.createParticleSystem('fountain'+s.app.getUniqueName(), self.particlename)        
        node.attachObject(particleSystem2)
        s.framelistener.addTimed(5,node,None)
        
        
class DamagePhysical():
    def __init__(self,damage,type):
        self.damage = damage
        self.type = type
    def execute(self,unit1,unit,endpos):
        damage = unit1.attributes.bravery * self.damage         
        unit.damageHitpoints(damage,self.type,unit1)
        
class DamageMagic():
    def __init__(self,damage,type):
        self.damage = damage
        self.type = type
    def execute(self,unit1,unit,endpos):    
        if unit:    
            unit.damageHitpoints(self.damage,self.type,unit1)
class AffectOther():
    def __init__(self,affect):
        self.affect = affect
    def execute(self,unit1,unit,endpos):
        if unit:    
            am = unit.affect        
            am.add(self.affect)