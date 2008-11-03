import sys
import copy
from tactics.Singleton import *
from tactics.Move import *
from tactics.datautil import *
from userinterface.HumanInterface import *
import ogre.gui.CEGUI as CEGUI
from utilities.CEGUI_framework import *
import utilities.SampleFramework as sf
s = Singleton()

class ItemHolder():
    def __init__(self):
        self.map = dict()
    def addItem(self,itemname):
        if self.map.has_key(itemname):
            self.map[itemname] += 1
        self.map[itemname] = 1
    
    def removeItem(self,itemname):
        if self.map.has_key(itemname):
            self.map[itemname] -= 1
            return True
           
class HumanPlayer(object):

    def __init__(self,name):
        self.name = name
        self.interface = HumanInterface(self)
        self.items =ItemHolder()
        
    def endTurn(self):
        s.turn.pause = False
        s.turn.nextUnitTurn()
        

        
    def setVisualMarker(self,unit):
        pos = unit.body.getOgreNode().getPosition()
        sceneManager = s.app.sceneManager        
        #self.startPos =position  
        #self.endPos.y = position.y
        name = s.app.getUniqueName()
        mesh = "ellipsoid.mesh"
    
        scene_node = unit.node.createChildSceneNode(name)
        attachMe = s.app.sceneManager.createEntity(name,mesh)            
        scene_node.attachObject(attachMe)
        attachMe.setNormaliseNormals(True)
    
        scene_node.position = Ogre.Vector3(0,2,0)
        scene_node.getAttachedObject(0).setMaterialName("LightGreen/SOLID")
                
        size = .3
        scene_node.scale = Ogre.Vector3(size,size,size)
        
    
    #Tells you what the id of the last cegui hooks for the framelistener was    
  
    
    unitlist = []
    cunit = None
    def startTurn(self,unit):
       self.cunit = unit 
       sf.Application.debugText = self.cunit.type
       #self.s.framelistener.cunit = cunit
       if not s.AIon:
           self.interface.cunit = self.cunit
           self.interface.displayActions()
       else:
           if unit.mental:
               for x in unit.mental.list:
                   if x.running:
                       if x.execute(0):
                           break;
                   
       
           
    
#    caction = None
#    def action(self,name):    
#        caction = name       
        #add hooks if hookid is different from last
     #   if click.hookid != hookid:
     #       setupInput()
    
    def clickEntity(self,name,position):
        
        self.interface.clickEntity(name,position)        
class ComputerPlayer(object):
    
    def __init__(self,name):
        self.name = name    
        self.unitlist = []
        self.itemlist = []
        self.items =ItemHolder()

    s = Singleton()
    def startTurn(self,unit):
        if unit.mental:        
            for x in unit.mental.list:
                if x.running:
                    if x.execute(0):
                        break;
        #unit.mental.map["combat"].execute(0)
        s.turn.pause = False    
        
        s.turn.nextUnitTurnUnpause()
        
        #go through playremap and find closest enemy.  Set to attack
       # a = 5       
    def clickEntity(self,name,position):
        if len(self.unitlist) > 0:
            return
        self.endGame()
    def endTurn(self):
        
        #CEGUI.WindowManager.getSingleton().destroyWindow("actionlist")
        s.turn.nextUnitTurn()           

