import ogre.renderer.OGRE as Ogre
import os
import shelve
import dbhash
import anydbm
import data.util
import tactics.util
 
import time
import data.overviewtrade
from tactics.Singleton import *
from utilities.physics import *
import ogre.gui.CEGUI as CEGUI
from utilities.CEGUI_framework import *
import tactics.util
import utilities.OgreText
import userinterface.util 


class AddDifferentPos:
    def __init__(self,pos):
        if isinstance(pos, tuple):
            self.poslist = [pos]
        else:
            self.poslist = pos
    def execute(self,timer):
        for x in self.poslist:
            cpos,next = x
            AddPos(cpos,s.overviewmap,next)


def addDots(vec1,vec2,slow = False):

    direction = vec2-vec1
    direction.normalise()

    while True:
        vec1 = vec1 + (direction * 1)
        rvec = data.util.getValidPos(vec1)
        
        
        if rvec:                             
            data.util.createMesh("cylinder.mesh", rvec, .5)
        
        if distance(vec1, vec2) < 2:
            return False
        
        if slow:
            return vec1
        

    
class Position:
    
    def __init__(self,vec,name,visited = False):
        self.plist = []
        #self.dllist = [] do later
        self.position = vec
        #self.node = None
        self.name = name
        self.node = None
        self.setVisited(visited)
        self.next = None
        
    
    def show(self):
        self.node =data.util.createMesh("cylinder.mesh",self.position,1,self.name)
        tactics.util.buildImmoblePhysics(self,self.node)
        self.setVisited(self.visited)
        s.framelistener.textlist.append(utilities.OgreText.OgreText(self.node.getAttachedObject(0),self.name))
        
    def getVec(self):
        x,y,z = self.position
        return Ogre.Vector3(x,y,z)
    def __str__( self ):
        return str(self.getVec())
    def setVisited(self,visited):
        self.visited = visited
        if self.node:
            if self.visited :
                self.node.getAttachedObject(0).setMaterialName( "LightBlue/SOLID" )
            else:
                self.node.getAttachedObject(0).setMaterialName( "BlueMage/SOLID" )
                
         
    def __getstate__(self):
        return {"name":self.name,"plist":self.plist,"position":self.position,"visited":self.visited,"next":self.next}
    def __setstate__(self,dict):
        self.__dict__ = dict
        self.node = None
        
class AddPos:
    def __init__(self,cpos,playermap,next = None):
        self.actionqueue=[]
        self.timeleft = 0
        if not next:
            self.next = cpos.next
        else:
            self.next = next
        if cpos.visited and (next or cpos.next):
            s.framelistener.unitqueue.addToQueue(self,self)
            playermap.map[self.next.name] = self.next
            playermap.addPos(cpos,self.next)
            self.cpos = cpos
            self.vec = self.cpos.getVec()
            self.timel = 0
            playermap.save()
            
        
            
        
    def execute(self,timer):
        if s.app.sceneManager.hasSceneNode(self.next.name):
            return False
        self.timel -= timer
        if self.timel < 0:            
            self.vec = addDots(self.vec,self.next.getVec(), True)
            s.playsound()
            if not self.vec and not self.next.visited:
                self.next.show()
                return False
            self.timel = 1
        return True
class SetVisited:
    def execute(self,timer):
        s.overviewmap.cpos.setVisited( True)
        if s.overviewmap.cpos.next and isinstance(s.overviewmap.cpos.next, Position): 
            AddPos(s.overviewmap.cpos,s.overviewmap)
        elif s.overviewmap.cpos.next:
            next =s.overviewmap.cpos.next
            
            next.execute(0)
            s.overviewmap.cpos.next = None
        
class OverviewMap:
    
    timeleft = 0
#    newgame = False
    newgame = True
    def __init__(self,text):
        self.map = dict()
        self.actionqueue=[]
        self.filename = "media\\saves\\"+text
        self.exitscene = None
        
        s.overviewmap = self
        s.framelistener.setCurrentPlayer( s.overviewmap)
        self.overviewtrade = data.overviewtrade.OverviewTrade()
        
        if os.path.exists(s.campaigndir+self.filename) and not self.newgame:
            positionmap = shelve.open(self.filename)
            #self.map = positionmap["map"]
            self.root,self.cpos = positionmap["mapdata"]
            
            s.cplayer = positionmap["unitdata"]
            s.playermap["Player1"] = s.cplayer
            #s.framelistener.setCurrentPlayer(s.cplayer)
            self.placetoscene = positionmap["placetoscene"]
            self.overviewtrade.load(positionmap)
            positionmap.close()
           # self.createLocations(self.root)
        else:
            if not s.editgame:
                s.settings.setupDefaultPositions(self)            

            #AddPos(self.root, self)
        #if file text exists then load positions from file
        
        #else setup default positions
        # load mesh 
        # for each pos create a big dot and call
        
#        camera = s.app.sceneManager.createCamera("wutwut")
        
#        camera.position = Ogre.Vector3(0,5,0)
        #camera.orientation = Ogre.Vector3.NEGATIVE_UNIT_Y
        #s.framelistener.setCurrentPlayer( = s.overviewmap
        s.app.loadScene("loadoverview")
        s.framelistener.setCurrentPlayer( self)
        #self.buildScene()
        s.app.menus.setupStartMenu()

    def loadScene(self, sceenname):
        s.framelistener.interrupt.append(LoadScene((sceenname)))
        s.framelistener.pauseturns = False
        self.overviewtrade.hide()
        userinterface.util.destroyWindow("Tesliz/MainMenuBackground")
        self.save()


    def save(self):
        positionmap = shelve.open(self.filename)
        positionmap["mapdata"] = self.root, self.cpos
        #positionmap["currentplayer"] = s.cplayer.name
        positionmap["placetoscene"] = self.placetoscene
        #print s.cplayer
        
        positionmap["unitdata"] =  s.playermap["Player1"]
        #positionmap["map"] = self.map
        self.overviewtrade.save(positionmap)
        positionmap.close()




        
        #used for
    def createLocations(self,root):
        
        if self.map.has_key(root.name):
            
            return
        else:
            
            self.map[root.name] = root
            s.app.sceneManager.getRootSceneNode().numChildren()
            root.show()
            
            
            for x in root.plist:
                addDots(root.getVec(),x.getVec())
                self.createLocations(x)
    

            
    #    for x in cpos.plist:
    #        self.addVisits(cpos)

    def addPos(self,pos1,pos2):
        pos1.plist.append(pos2)
        pos2.plist.append(pos1)
        

    def movePlayer(self,pos):
       pass 
   
    def clickEntity(self,name,position,id,evt):
       if not self.map.has_key(name):
           return
       
       exitname = self.cpos.name+"-Exit"
       if self.placetoscene.has_key(exitname) and self.cpos.visited:
           self.loadScene(self.placetoscene[exitname])
           self.exitscene = exitname
           return
       self.move = data.traits.basictraits.FFTMove()
       self.move.unit1 = self.unit
       self.move.endPos = position
       self.move.list = self.getMoveList(self.cpos,self.map[name])
       self.cpos = self.map[name]
       for x in self.move.list:
           print x
       print "aoue"
       s.framelistener.unitqueue.addToQueue(self,self)
    
    def execute(self,timer):
        if not self.move.execute(timer):
            
            if not self.cpos.visited:
                
                sceenname = self.cpos.name
                if self.placetoscene.has_key(self.cpos.name):
                    sceenname = self.placetoscene[self.cpos.name]
                self.loadScene(sceenname)
                return False
            
            self.overviewtrade.show(self.cpos.name)
            return False
        return True
    
    def currentVisited(self,winningplayer):
        #data.util.clearMeshes()
        self.save()
        if self.exitscene:
            del self.placetoscene[self.exitscene]
            self.exitscene = None
        #self.buildScene()
        
        
        s.framelistener.setCurrentPlayer( self)
        #s.turn.pause = True
        
        
        s.framelistener.interrupt.append(LoadScene(("loadoverview")))
        if winningplayer == "Player1":
            s.framelistener.interrupt.append(SetVisited())
        
        self.overviewtrade.show(self.cpos.name)
        s.app.menus.setupStartMenu()
        s.framelistener.setCurrentPlayer( self)
        
    def getMoveList(self,cpos,topos,movedlist =[],posset = None):
        if not posset:
            posset = set()
        posset.add(cpos)
        if cpos == topos:
            return [topos.getVec()]
        for pos in cpos.plist:
            if pos in posset:
                continue
            rpos =self.getMoveList(pos,topos,movedlist,posset)
            if rpos:
                rpos.insert(0,cpos.getVec())
                return rpos
    
        