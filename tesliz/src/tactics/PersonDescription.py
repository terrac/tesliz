import ogre.renderer.OGRE as Ogre
import data.util


class PersonDescription:
    head = None
    torso = None
    legs = None
    hair = None
    nodelist =[head,torso,legs,hair]
    
    def setup(self,position,head,torso,legs,hair,torsolength,torsowidth,leglength,facetexture,torsotexture):
        
        self.torso = data.util.createMesh(torso, position)        
        self.legs = data.util.createMesh(legs, Ogre.Vector3(0,-1,0))
        self.torso.addChild(self.legs)
        self.head = data.util.createMesh(head, Ogre.Vector3(0,1,0))
        self.torso.addChild(self.head)
        self.hair = data.util.createMesh(hair, Ogre.Vector3(0,1,0))
        self.head.addChild(self.hair)
        
        self.torso.setScale(Ogre.Vector3(torsowidth,torsolength,torsowidth))
        self.legs.setScale(Ogre.Vector3(1,leglength,1))
        
    def animateSetup(self,name,sound):
        self.animationState = []
        for node in nodelist:
            entity = node.getAttachedObject(0)
            if entity:
                animation = entity.getAnimationState(name)
                self.animationState.append(animation)
                animation.setLoop(True)
                animation.setEnabled(True)
            self.sound =s.playsound(sound,option="loop")    
    def animate(self,timer):    
        for animation in self.animationState:        
            animation.addTime(timer)
            
    def stopAnimation(self):
        if self.sound:
            self.sound.stop()
        for animation in self.animationState:
            animation.setTimePosition(0);
        
    