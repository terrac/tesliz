from tactics.Singleton import *
import ogre.renderer.OGRE as Ogre
#import data.traits.generictraits 
#import data.traits.generictraits as GenericTraits
import data.util
import ogre.physics.OgreNewt as OgreNewt
import tactics.Material
import damage
s = Singleton()
import copy
import data.Affects
class Particle:
    def __init__(self, name,time = 5,turns = False,sound=None,showempty = False):
        self.showempty = showempty
        self.particlename = name
        self.time = time
        self.sound = sound
    def execute(self,unit1,unit,endpos):
    
        if not unit and not self.showempty:
            return
            
        name = s.app.getUniqueName()
        
        node = s.app.sceneManager.getRootSceneNode().createChildSceneNode( name + "Node" )
        node.setPosition(Ogre.Vector3(endpos.x,endpos.y,endpos.z))
        psm = Ogre.ParticleSystemManager.getSingleton()

        particleSystem2 = s.app.sceneManager.createParticleSystem('fountain'+s.app.getUniqueName(), self.particlename)        
        node.attachObject(particleSystem2)
        s.framelistener.addTimed(self.time,node,None)
        if self.sound:
            s.playsound(self.sound)

class Throw():
    def __init__(self, item = None,getDamage = None):
        self.run = False
        self.item = item
        if isinstance(item, str):
            self.mesh = item
            self.getDamage = getDamage
            self.do = lambda self,unit2: data.util.damageHitpoints(getDamage,self.unit1,unit2)
        else:
            self.mesh = item.mesh
            self.do = lambda self,unit2: unit2.items.do(self.item.affects)
        
    
    
        
    def onContact(self,contactname):
        if not self.run:
            return 0
        unit = s.unitmap[contactname]
        
        s.app.sceneManager.getRootSceneNode().removeChild(self.node)
        
        self.do(self,unit)
        
        self.run=False
        return 0
    def execute(self,unit1,unit2,endpos):
        self.run = True
        
        vector1 = unit1.body.getOgreNode().getPosition()
        
        self.unit1 = unit1
        if unit2 and unit2.body:
            vector2 = unit2.body.getOgreNode().getPosition()
        else:
            endpos.y = vector1.y
            vector2 = endpos    
        World = s.app.World
        sceneManager = s.app.sceneManager
        #vector1.y += 5
        direction = vector2 - vector1
        direction.normalise()
        vector1 = vector1 +direction * 2
        
        name = s.app.getUniqueName()
        
        node = sceneManager.getRootSceneNode().createChildSceneNode( name + "Node" )
                        
        data.util.createEntity(self.mesh,node)

        node.setPosition(0.0, 0.0, 0.0)
        node.setScale(0.1,0.1,0.1)      
        col = OgreNewt.Cylinder(World, .5, .5)
        body = OgreNewt.Body( World, col)
        material =tactics.Material.Material(name,data.traits.generictraits.ObjectCallback( 2))
        body.setMaterialGroupID( material.MatObject )
        body.setType(2)
        body.setUserData(self)
        del col
        inertia = OgreNewt.CalcSphereSolid( 10.0, 1.0 )
        body.setMassMatrix( 1.0, inertia )
        body.attachToNode( node )
        body.setStandardForceCallback()
        body.setPositionOrientation( vector1, unit1.body.getOgreNode().getOrientation() )
        body.setVelocity( (direction * 55.0) )
        s.framelistener.addTimed(5,node,body,self)
        s.framelistener.timer = 2
        self.node = node
        return False

#it should be used not removed
#class RemoveItem():
#    def __init__(self,potionname):
#        self.potionname = potionname
        
#    def execute(self,unit1,unit,endpos):
#        return unit1.player.items.removeItem(self.potionname)
                    
class RibbonTrail1():
    def __init__(self, name):
        self.name = name
        
    def execute(self,unit1,unit,endpos):
        
        pairList = Ogre.NameValuePairList()
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
        anim.setInterpolationMode(Ogre.Animation.IM_SPLINE)
        track = anim.createNodeTrack(1, animNode)
        kf = track.createNodeKeyFrame(0)
        kf.Translate=Ogre.Vector3(50,30,0)
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
        
        pairList = Ogre.NameValuePairList()
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
        anim.setInterpolationMode(Ogre.Animation.IM_SPLINE)
        track = anim.createNodeTrack(1, animNode)
        kf = track.createNodeKeyFrame(0)
        color = Ogre.ColourValue(0,0,1,1)
        bbs = sceneManager.createBillboardSet(s.app.getUniqueName(), 1)
        bbs.createBillboard(Ogre.Vector3.ZERO, color)
        bbs.MaterialName="Examples/Flare"
        bbs.setDefaultDimensions(1, 1); 
        animNode.attachObject(bbs)
        
        endpos.y += 5
        endpos.x += 1
        
        
        kf.Translate=Ogre.Vector3(endpos)
        kf = track.createNodeKeyFrame(2)
        
        endpos.y += 5
        endpos.x += -2
        
        kf.Translate=Ogre.Vector3(endpos)
        kf = track.createNodeKeyFrame(4)
        endpos.y += 5
        endpos.x += -2
        
        #kf.Translate=Ogre.Vector3(endpos)
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
        self.getDamage = damage
        self.type = type
    def execute(self,unit1,unit,endpos):
        if unit:
            damage = unit1.attributes.bravery * self.getDamage         
            unit.damageHitpoints(damage,self.type,unit1)
        
class DamageMagic():
    def __init__(self,damage,type = None):
        self.getDamage = damage
    
    def execute(self,unit1,unit,endpos):    
        if unit:    
            data.util.damageHitpoints(self.getDamage, unit1, unit)
            #unit.damageHitpoints(self.getDamage,self.type,unit1)
    
        
class AffectOther():
    def __init__(self,affect):
        self.affect = affect
    def execute(self,unit1,unit,endpos):
        if unit:    
            am = unit.affect        
            am.add(self.affect)

class RemoveItem():
    def __init__(self,itemname):            
        self.itemname = itemname
    def execute(self,unit1,unit,endpos):
        return unit1.player.items.removeItem(self.itemname)    
       # s.screenshot()
       
class AffectLand():
    def __init__(self,affectname):
        self.affectname = affectname
    def execute(self,unit1,unit,endpos):
        #build node with the name of the affect
        endpos = endpos * 1
        endpos.y += 2
        name =data.util.show(endpos,"Ta/SOLID",self.affectname+"-"+s.app.getUniqueName(),.6)
        unit1.addTurned(0,s.app.sceneManager.getSceneNode(name),None)
        
        if unit:    
            unit.affect.add( data.Affects.affectmap[self.affectname])        
            unit.traits.Move[0].affect = data.Affects.affectmap[self.affectname]