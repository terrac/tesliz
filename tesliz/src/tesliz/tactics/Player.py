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

class PlayerItemHolder():
        
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
    def itemNum(self,itemname):
        if self.map.has_key(itemname):
            return self.map[itemname]
        return 0
    def __str__( self ):
        return str(self.map)
    
class HumanPlayer(object):

    def addToUnitlist(self,unit):
        for x in self.unitlist:
            if x.name == unit.name:
                raise Exception("unit already in list")
        self.unitlist.append(unit)
    def __getstate__(self):
        return {"name":self.name,"items":self.items,"unitlist":self.unitlist}
    def __setstate__(self,dict):
        self.__dict__ = dict
        self.interface = HumanInterface(self)
    def __str__(self):
        return self.name + str(self.items) +"\n"+str(printlist(self.unitlist))
    def __init__(self,name):
        self.name = name
        self.interface = HumanInterface(self)
        self.items =PlayerItemHolder()
        self.unitlist = []
        self.cunit = None
    def endTurn(self):
        s.turn.pause = False
        s.turn.nextUnitTurn()
        

        
    def setVisualMarker(self,unit):
        pos = unit.node.getPosition()
        sceneManager = s.app.sceneManager        
        #self.startPos =position  
        #self.endPos.y = position.y
        name = s.app.getUniqueName()
        mesh = "ellipsoid.mesh"
    
        scene_node = unit.node.createChildSceneNode(name)
        attachMe = s.app.sceneManager.createEntity(name,mesh)            
        scene_node.attachObject(attachMe)
        #attachMe.setNormaliseNormals(True)
    
        scene_node.position = Ogre.Vector3(0,2,0)
        scene_node.getAttachedObject(0).setMaterialName("LightGreen/SOLID")
                
        size = .3
        scene_node.setScale( Ogre.Vector3(size,size,size))
        
    
    #Tells you what the id of the last cegui hooks for the framelistener was    
  
    

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
                   s.framelistener.unitqueue.addToQueue(unit,x)
                   
       
           
    
#    caction = None
#    def action(self,name):    
#        caction = name       
        #add hooks if hookid is different from last
     #   if click.hookid != hookid:
     #       setupInput()
    
    def clickEntity(self,name,position,id,evt):
        
        self.interface.clickEntity(name,position,id,evt)        
class ComputerPlayer(object):
    def addToUnitlist(self,unit):
        for x in self.unitlist:
            if x.name == unit.name:
                raise Exception("unit already in list")
        self.unitlist.append(unit)
    def __init__(self,name):
        self.name = name    
        self.unitlist = []
        self.itemlist = []
        self.items =PlayerItemHolder()

    s = Singleton()
    def startTurn(self,unit):
        if s.framelistener.pauseturns:
            return
        if unit.mental:        
            for x in unit.mental.list:
                s.framelistener.unitqueue.addToQueue(unit,x)
        
        s.turn.pause = False    
        
        s.turn.nextUnitTurnUnpause()
        
        #go through playremap and find closest enemy.  Set to attack
       # a = 5       
    def clickEntity(self,name,position,id,evt):
        if len(self.unitlist) > 0:
            return
        self.endGame()
    def endTurn(self):
        
        #CEGUI.WindowManager.getSingleton().destroyWindow("actionlist")
        s.turn.nextUnitTurn()           

