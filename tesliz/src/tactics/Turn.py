from tactics.Singleton import *
import logging
log = logging.getLogger('')
s = Singleton()

def show(unit):
    pos = unit.body.getOgreNode().getPosition()
    sceneManager = s.app.sceneManager        
    name = "turncircle"
    mesh = "cylinder.mesh"
    if not sceneManager.hasSceneNode(name):
        scene_node = sceneManager.rootSceneNode.createChildSceneNode(name)
        attachMe = s.app.sceneManager.createEntity(name,mesh)            
        scene_node.attachObject(attachMe)
        attachMe.setNormaliseNormals(True)
    else:
        scene_node = sceneManager.getSceneNode(name)
    scene_node.position = Ogre.Vector3(pos.x,pos.y+5,pos.z)
    
    size = 1
    scene_node.scale = Ogre.Vector3(size,size,size)
    
    scene_node.rotate(Ogre.Quaternion(Ogre.Degree(90), Ogre.Vector3.UNIT_Z))
    
   
class Turn(object):
    
    
    
    pnum = 0
    
    def __init__(self):
        s.turn = self
        
    pause = False    
    def doTurn(self):

        if self.pause:
            return
        if len(self.turnlist) > 0:
            self.nextUnitTurn()
            return
        
        for unit in s.unitmap.values():
            
            if unit.increment():
               self.turnlist.append(unit) 
               
    def nextUnitTurnUnpause(self):
        self.pause = False
        self.nextUnitTurn()    
    def nextUnitTurn(self):
        if not s.framelistener.getActiveQueue() == 0:        
            return
        if (s.framelistener.timer > 0.0) or s.ended or self.pause:
            return
        if len(self.turnlist)== 0:
            return
        
      #  for x in s.unitmap.values():
      #      x.body.freeze()      
        self.pause = True
        s.framelistener.timer = 1
        unit =self.turnlist.pop()
        if unit.attributes.hitpoints <1:
            self.pause  = False
            return
            
        s.log(unit)
        s.framelistener.cplayer = unit.player
        
    
        show(unit)
        unit.startTurn()
                   
    turnlist = []          
        
        
            
        
         
class RealTimeTurn(object):
    def __init__(self):
        s.turn = self
        
    def doTurn(self):
        pass
        #self.pause = False
#        if len(s.framelistener.unitqueues) == 0:
#            for player in s.playermap.values():
#                for unit in player.unitlist:
#                    unit.startTurn()
                    #show(unit)
                    #break
    def nextUnitTurn(self):
        s.framelistener.cplayer = s.playermap["Player1"]
        
    def nextUnitTurnUnpause(self):
        #self.pause = False
        self.nextUnitTurn()                        