from tactics.Singleton import *
import ogre.renderer.OGRE as ogre
s = Singleton()
import copy
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
        
class RibbonTrail1():
    def __init__(self, name):
        self.name = name
        
    def execute(self,unit1,unit,endpos):
        
        pairList = ogre.NameValuePairList()
        pairList['numberOfChains'] = '2'
        pairList['maxElements'] = '80'
        sceneManager = s.app.sceneManager
        trail=sceneManager.createMovableObject(s.app.getUniqueName(), "RibbonTrail", pairList)    # this returns a ribbontrail object
        trail.setMaterialName ("Examples/LightRibbonTrail")
        trail.setTrailLength (200)

        # attach Ribbon Trail scene node
        sceneManager.getRootSceneNode().createChildSceneNode().attachObject(trail)

        #Create 3 nodes for trail to follow
        animNode = sceneManager.getRootSceneNode().createChildSceneNode()
        animNode.setPosition(endpos)
        ani = s.app.getUniqueName()
        anim = sceneManager.createAnimation(ani, 14)
        anim.setInterpolationMode(ogre.Animation.IM_SPLINE)
        track = anim.createNodeTrack(1, animNode)
        kf = track.createNodeKeyFrame(0)
        kf.Translate=ogre.Vector3(50,30,0)
        kf = track.createNodeKeyFrame(2)

        animState = sceneManager.createAnimationState(ani)
        animState.Enabled=True
        s.app.animations.append(animState)

        trail.setInitialColour(0, 1.0, 0.8, 0.4)
        trail.setColourChange(0, 0.5, 0.5, 0.5, 0.5)
        trail.setInitialWidth(1, 1)
        trail.addNode(animNode)

        #Add light
        l2 = sceneManager.createLight(s.app.getUniqueName())
        l2.setDiffuseColour(trail.getInitialColour(0))
        animNode.attachObject(l2)
class RibbonTrail():
    def __init__(self, name):
        self.name = name
        
    def execute(self,unit1,unit,endpos):
        
        pairList = ogre.NameValuePairList()
        pairList['numberOfChains'] = '2'
        pairList['maxElements'] = '8'
        sceneManager = s.app.sceneManager
        #trail=sceneManager.createMovableObject(s.app.getUniqueName(), "RibbonTrail", pairList)    # this returns a ribbontrail object
        #trail.setMaterialName ("Examples/LightRibbonTrail")
        #trail.setTrailLength (2)

        # attach Ribbon Trail scene node
        #node = sceneManager.getRootSceneNode().createChildSceneNode()
        #node.attachObject(trail)

        #Create 3 nodes for trail to follow
        animNode = sceneManager.getRootSceneNode().createChildSceneNode()
        animNode.setPosition(endpos)
        ani = s.app.getUniqueName()
        anim = sceneManager.createAnimation(ani, 14)
        anim.setInterpolationMode(ogre.Animation.IM_SPLINE)
        track = anim.createNodeTrack(1, animNode)
        kf = track.createNodeKeyFrame(0)
        color = Ogre.ColourValue(0,0,1,1)
        bbs = sceneManager.createBillboardSet(s.app.getUniqueName(), 1)
        bbs.createBillboard(ogre.Vector3.ZERO, color)
        bbs.MaterialName="Examples/Flare"
        bbs.setDefaultDimensions(1, 1); 
        animNode.attachObject(bbs)
        
        endpos.y += 5
        endpos.x += 1
        
        
        kf.Translate=ogre.Vector3(endpos)
        kf = track.createNodeKeyFrame(2)
        
        endpos.y += 5
        endpos.x += -2
        
        kf.Translate=ogre.Vector3(endpos)
        kf = track.createNodeKeyFrame(4)
        endpos.y += 5
        endpos.x += -2
        
        #kf.Translate=ogre.Vector3(endpos)
        #kf = track.createNodeKeyFrame(6)

        animState = sceneManager.createAnimationState(ani)
        animState.Enabled=True
        #animState.Loop = False
        #animState.TimePosition = .5
        
        s.app.animations.append(animState)
        s.framelistener.addTimed(2,animNode)

        #trail.setInitialColour(0, 0, 1, .5)
        #trail.setColourChange(0, 0.5, 0.5, 0.5, 0.5)
        #trail.setInitialWidth(0,1)
        #trail.addNode(animNode)
        

        #Add light
        l2 = sceneManager.createLight(s.app.getUniqueName())
        l2.setDiffuseColour(color)
        animNode.attachObject(l2)
        #animNode.setScale(.1,.1,.1)
        
        
        
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
            
            
            