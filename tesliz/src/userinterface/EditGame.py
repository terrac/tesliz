import ogre.renderer.OGRE as Ogre
import ogre.addons.et as ET
import ogre.io.OIS as OIS
import ogre.gui.CEGUI as CEGUI
import exceptions, random, os
import ogre.physics.OgreNewt as OgreNewt
from tactics.Singleton import *
import util
import tactics.util
import data.util
import shelve
 
import utilities.FollowCamera
import tactics.Unit
import copy
import tactics.Building
import manager.gridmap

def getFromFile(filename):
    module = __import__("data.maps."+filename)
    module = getattr(module,'maps')
    map = getattr(module,filename).Unitdata()
    return map.getEvents()

class EditGame:
    mapname = "media\\et\\"
    def getMapName(self):
        return s.campaigndir+self.name +"\\mapdata.dat"
    def __init__(self,name ):
        self.name = name
        s.terrainmanager.loadTerrain(name)
        s.app.msnCam.setOrientation(Ogre.Quaternion(-1,0,0,0))
        #destroy and save current layout
        s.cegui.hide()
        s.framelistener.unitqueue.clearUnitQueue()
        s.framelistener.pauseturns = True
        s.framelistener.cplayer =self
        s.editgame = self
        
        savedmap = None
        
        if os.path.exists(self.getMapName()):
            savedmap = shelve.open(self.getMapName())
#        else:
#        
#            savedmap = shelve.open(self.getMapName())
#            map,convo = getFromFile(name)
#            savedmap["unitmap"] =map
#            positionmap = dict()
#            for x in map:
#                if map[x].node:
#                    positionmap[x] = map[x].node.getPosition()
#            savedmap["positionmap"] = positionmap
#            
#            scriptmap = dict()
#            scriptmap["script01"] = convo
#            savedmap["scriptmap"] = scriptmap 
            
        #create cegui layout
        
        #mmb = util.getNewWindow( "EditMenu", "root_wnd", "TaharezLook/FrameWindow")
#        sheet.addChildWindow(mainMenuBackground)
#        mmb.setPosition(CEGUI.UVector2(cegui_reldim(0.75), cegui_reldim( 0.10)))
#        mmb.setSize(CEGUI.UVector2(cegui_reldim(0.24), cegui_reldim( 0.74)))
#        mainMenuBackground.setCloseButtonEnabled(false)
#        mainMenuBackground.setText("Tesliz Menu Frame")
#
        tbc =util.getNewWindow("TabMenu","TaharezLook/TabControl","root_wnd")
        
        #tbc.setSize(CEGUI.UVector2(cegui_reldim(1), cegui_reldim( 0.24)))
        tbc.setPosition(CEGUI.UVector2(cegui_reldim(0.75), cegui_reldim( 0.10)))
        tbc.setSize(CEGUI.UVector2(cegui_reldim(0.24), cegui_reldim( 0.74)))
        tbc.subscribeEvent(CEGUI.TabControl.EventSelectionChanged, self, "setCurrentTab")
        terrain =s.cegui.winMgr.createWindow("DefaultGUISheet", "Terrain")
        terrain.setText("Terrain")
        tbc.addTab(terrain)
        self.editterrain = EditTerrain(terrain)
        self.currentClick = self.editterrain
#        
        tab2 =s.cegui.winMgr.createWindow("DefaultGUISheet", "Units")
        tab2.setText("Units")
        tbc.addTab(tab2)
        self.editunits = EditUnits(tab2,savedmap)
        #self.currentClick = self.editunits
        
        tab3 =s.cegui.winMgr.createWindow("DefaultGUISheet", "Scripts")
        tab3.setText("Scripts")
        tbc.addTab(tab3)
        self.editscripts = EditScripts(tab3,savedmap)
        #self.currentClick = self.editscripts
        
        tab4 =s.cegui.winMgr.createWindow("DefaultGUISheet", "Meshes")
        tab4.setText("Meshes")
        
        tbc.addTab(tab4)
        self.editmeshes = EditMeshes(tab4,savedmap)    

        btn = util.getNewWindow("save", "TaharezLook/Button", "root_wnd")
        
        btn.setText("save")
        btn.setPosition(CEGUI.UVector2(cegui_reldim(0.835), cegui_reldim( 0.85)))
        btn.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.05)))
        btn.subscribeEvent(CEGUI.PushButton.EventClicked, self, "saveGame")

#        btn = util.getNewWindow("reload", "TaharezLook/Button", "root_wnd")
#        
#        btn.setText("reload")
#        btn.setPosition(CEGUI.UVector2(cegui_reldim(0.735), cegui_reldim( 0.85)))
#        btn.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.05)))
#        btn.subscribeEvent(CEGUI.PushButton.EventClicked, self, "loadGame")             
        if savedmap:
            savedmap.close()

    def clickEntity(self,name,position,id,evt):
        self.currentClick.clickEntity(name, position, id, evt)


    def setCurrentTab(self, e):
        if not e.window.getActiveChild():
            return True
        text = str(e.window.getActiveChild().getText())
        if hasattr(self.currentClick, "close"):
            self.currentClick.close()
        if text == "Terrain":
            self.currentClick = self.editterrain
        if text == "Units":
            self.currentClick = self.editunits
        if text == "Scripts":
            self.currentClick = self.editscripts
        if text == "Meshes":
            self.currentClick = self.editmeshes
        return True
    def saveGame(self,e):
        s.terrainmanager.saveTerrain(self.name)
        
        savedmap = shelve.open(self.getMapName())
        
        for x in self.editunits.unitmap.values():
            x.node = None
            x.body = None
        savedmap["unitmap"] = self.editunits.unitmap
        savedmap["positionmap"] = self.editunits.positionmap
        savedmap["scriptmap"] = self.editscripts.scriptmap
        savedmap.close()
#    def loadGame(self,e = None):
#        s.terrainmanager.loadTerrain(self.name)
#        for unit in s.editgame.editunits.unitmap.values():
#            if unit.node:
#                position = data.util.getValidPos(unit.node.getPosition())
#                unit.node.setPosition(position)
#                s.editgame.editunits.positionmap[unit.node.getName()] = (position.x,position.y,position.z)
class EditTerrain():
    def __init__(self,pwindow):
               
        self.deformbtn =btn = CEGUI.WindowManager.getSingleton().createWindow("TaharezLook/Button", "deform")
        pwindow.addChildWindow(btn)
        btn.setText("deform")
        self.deform = True
        #btn.setPosition(CEGUI.UVector2(cegui_reldim(0.7), cegui_reldim( 0.0)))
        btn.setSize(CEGUI.UVector2(cegui_reldim(0.5), cegui_reldim( .1)))
        btn.subscribeEvent(CEGUI.PushButton.EventClicked, self, "deformChange")        
        #image = Ogre.Image()
        #image.load("brush.png", "ET")
        name = "brush"
        #y = .1
        brushlist =["SmallBrush","InvertedTriangle","LargeBrush"]
        y = .1
        for name in brushlist:
            self.addItem(name,y,pwindow,"setBrushImage")
            y += .1
        self.texlist =["Rock","Grass"]
        
        x = 0
        for name in self.texlist:
            self.addItem(name,y,pwindow,"setTexture")
            y += .1
           # textures[i].load("splatting%s.%s" %( str(x), "png" ) , "ET")
       # baseTexture = ogre.Image()
       
     #   s.terrainmanager.splatMgr.createBaseTexture(baseTexture, 512, 512, textures, 20, 20)
        
     #   baseTexture.save(os.path.join(self.mediadir,"ET/ETbase.png"))
        
        self.setBrushImage("SmallBrush")
        self.texture = "Rock"

        
        
    def addItem(self, name, y,terrain,eventHandler):
        staticImg = s.cegui.getStaticImage(name + ".png", "ET")
        staticImg.setPosition(CEGUI.UVector2(cegui_reldim(0.0), cegui_reldim(y)))
        staticImg.setSize(CEGUI.UVector2(cegui_reldim(.5), cegui_reldim(0.1)))
        staticImg.setText(name)
        terrain.addChildWindow(staticImg)
        tex = util.getNewWindow(name + "st", "TaharezLook/StaticText")
        tex.setText(name)
        tex.setPosition(CEGUI.UVector2(cegui_reldim(0.5), cegui_reldim(y)))
        tex.setSize(CEGUI.UVector2(cegui_reldim(.5), cegui_reldim(0.1)))
        terrain.addChildWindow(tex)
        tex.subscribeEvent(CEGUI.Window.EventMouseClick, self, eventHandler)
        staticImg.subscribeEvent(CEGUI.Window.EventMouseClick, self, eventHandler)
        

    
    def deformChange(self, e):        
        
        
        self.setDeform(not self.deform) 
        
        return True    
    
    def setDeform(self,deform):
        self.deform = deform
        if self.deform:
            self.deformbtn.setText("Deform")
        else:
            self.deformbtn.setText("Paint")
        return True

    def setBrushImage(self,e):
        if isinstance(e, str):
            text = e
        else:
            text = e.window.getText()
        image = Ogre.Image()
        image.load(str(text)+".png", "ET")
        #image.resize(5,5)
        self.mEditBrush = ET.loadBrushFromImage(image)
        return True
    def setTexture(self,e):
        
        self.texture = str(e.window.getText())
        self.setDeform(False)
        return True
                                        
    def clickEntity(self,name,position,id,evt):

        
        x = int( s.terrainmanager.getTerrainInfo().posToVertexX(position.x) )
        z = int( s.terrainmanager.getTerrainInfo().posToVertexZ(position.z) )
        dr = -1
        
        if ( id == OIS.MB_Left ):
            dr = 1
        intensity = 1 * dr
        if self.deform:
            s.terrainmanager.terrainMgr.deform(x,z, self.mEditBrush,intensity)
            s.terrainmanager.terrainMgr.getTerrainInfo()
            for unit in s.editgame.editunits.unitmap.values():
                if unit.node:
                    position = manager.gridmap.getPositions(unit.node.getPosition())[0]
                    unit.node.setPosition(position)
                    s.editgame.editunits.positionmap[unit.node.getName()] = (position.x,position.y,position.z)

        else:
            s.terrainmanager.splatMgr.paint(self.texlist.index(self.texture), x, z, self.mEditBrush, 1)
            
            
        s.terrainmanager.generateTerrainCollision()
class EditUnits:
    selectedItem = None
    def __init__(self,pwindow,savedmap):    
            
        y = 0
        self.selectedunit =tex = util.getNewWindow("selectedunit", "TaharezLook/StaticText")
        tex.setText("")
        tex.setPosition(CEGUI.UVector2(cegui_reldim(0), cegui_reldim(y)))
        tex.setSize(CEGUI.UVector2(cegui_reldim(1), cegui_reldim(0.08)))
        pwindow.addChildWindow(tex)
        
        y += .1
        self.unitname =eb = s.cegui.winMgr.createWindow("TaharezLook/Editbox", "unitname")
        pwindow.addChildWindow(eb)
        eb.setPosition(CEGUI.UVector2(cegui_reldim(0.0), cegui_reldim( y)))
        #eb.setMaxSize(CEGUI.UVector2(cegui_reldim(1.0), cegui_reldim( 0.04)))
        eb.setSize(CEGUI.UVector2(cegui_reldim(0.50), cegui_reldim( 0.08)))
        eb.setText("namehere")
        tex = util.getNewWindow("unitnamedesc", "TaharezLook/StaticText")
        tex.setText("UnitName")
        tex.setPosition(CEGUI.UVector2(cegui_reldim(.5), cegui_reldim(y)))
        tex.setSize(CEGUI.UVector2(cegui_reldim(.5), cegui_reldim(0.08)))
        pwindow.addChildWindow(tex)
        
        y += .1
        self.unittype =unittypes = s.cegui.winMgr.createWindow("TaharezLook/Combobox", "unittypes")
        pwindow.addChildWindow(unittypes)        
        #unittypes.setText("actionlist")
        unittypes.setPosition(CEGUI.UVector2(cegui_reldim(0), cegui_reldim( y)))
        unittypes.setSize(CEGUI.UVector2(cegui_reldim(1), cegui_reldim( 0.4)))
        
        util.addItem(self, unittypes, "Squire")
        util.addItem(self, unittypes, "Chemist")
        util.addItem(self, unittypes, "Wizard")
        unittypes.setText("Squire")
        
        
        y += .1
        self.unitplayer =unitplayers = s.cegui.winMgr.createWindow("TaharezLook/Combobox", "unitPlayer")
        pwindow.addChildWindow(unitplayers)        
        #unitplayers.setText("actionlist")
        unitplayers.setPosition(CEGUI.UVector2(cegui_reldim(0), cegui_reldim( y)))
        unitplayers.setSize(CEGUI.UVector2(cegui_reldim(1), cegui_reldim( 0.4)))
        util.addItem(self, unitplayers, "Player1")
        util.addItem(self, unitplayers, "Computer1")        
        unitplayers.setText("Player1")
        
        y += .1
        self.unitlevel =eb = s.cegui.winMgr.createWindow("TaharezLook/Editbox", "level")
        pwindow.addChildWindow(eb)
        eb.setPosition(CEGUI.UVector2(cegui_reldim(0.0), cegui_reldim( y)))
        #eb.setMaxSize(CEGUI.UVector2(cegui_reldim(1.0), cegui_reldim( 0.04)))
        eb.setSize(CEGUI.UVector2(cegui_reldim(0.50), cegui_reldim( 0.08)))
        eb.setText("1")
        
        tex = util.getNewWindow("leveldesc", "TaharezLook/StaticText")
        tex.setText("Level")
        tex.setPosition(CEGUI.UVector2(cegui_reldim(.5), cegui_reldim(y)))
        tex.setSize(CEGUI.UVector2(cegui_reldim(.5), cegui_reldim(0.08)))
        pwindow.addChildWindow(tex)
         
        y +=.1
        btn = CEGUI.WindowManager.getSingleton().createWindow("TaharezLook/Button", "createunit")
        pwindow.addChildWindow(btn)
        btn.setText("Create")
        btn.setPosition(CEGUI.UVector2(cegui_reldim(0.2), cegui_reldim(y)))
        btn.setSize(CEGUI.UVector2(cegui_reldim(0.5), cegui_reldim( .1)))
        btn.subscribeEvent(CEGUI.PushButton.EventClicked, self, "createUnit")  
        
        y += .1
          
        if savedmap:
            self.unitmap = savedmap["unitmap"]
            self.positionmap = savedmap["positionmap"]
        else:
            self.unitmap = dict()
            #self.unitmap["dummy"] = tactics.util.buildUnitNoNode("dummy","Player1", "Squire")
            
            #self.positionmap = dict()
            #self.positionmap["dummy"] = (0,0,0)
        for name in s.unitmap.keys():
            if not self.unitmap.has_key(name):
                self.unitmap[name] = s.unitmap[name] 
        for name in self.unitmap.keys():
            if self.positionmap.has_key(name):
                position =self.positionmap[name]
                tactics.util.showUnit(self.unitmap[name],position)
        self.unitlist = unitlist = s.cegui.winMgr.createWindow("TaharezLook/Combobox", "unitlist")
        pwindow.addChildWindow(unitlist)        
        #unitlist.setText("actionlist")
        unitlist.setPosition(CEGUI.UVector2(cegui_reldim(0), cegui_reldim( y)))
        unitlist.setSize(CEGUI.UVector2(cegui_reldim(1), cegui_reldim( 0.2)))
        for x in self.unitmap.keys():
            util.addItem(self, unitlist, x)
        unitlist.subscribeEvent(CEGUI.Combobox.EventTextSelectionChanged, self, "setCurrentName")

        y += .1
        
        btn =util.getNewWindow("deleteunit", util.button,pwindow, .2, y, .5, .1, "delete")
        btn.subscribeEvent(CEGUI.PushButton.EventClicked, self, "deleteUnit")
        

        
        
    def setCurrentName(self,e):
        if not e.window.getSelectedItem():
            return
        text = str(e.window.getSelectedItem().getText())
        item =e.window.getSelectedItem()
        self.selectedunit.setText(text)
        self.selectedItem = item
    def createUnit(self,e):
        text =str(self.unitname.getText())
        type = str(self.unittype.getText())
        level = int(str(self.unitlevel.getText()))
        player = str(self.unitplayer.getText())
        util.addItem(self, self.unitlist, text)
        self.unitmap[text] =tactics.util.buildUnitNoNode(text,player, type,)
        self.selectedunit.setText(text)
        
    def deleteUnit(self,e):
        if self.selectedItem:        
            self.unitlist.removeItem(self.selectedItem)
            text = str(self.selectedItem.getText())
            del self.unitmap[text] 
            del self.positionmap[text] 
    def clickEntity(self,name,position,id,evt):
        name = str(self.selectedunit.getText())
        if not self.unitmap.has_key(name):
            return True
        self.positionmap[name] = (position.x,position.y,position.z)
        tactics.util.showUnit(self.unitmap[name], position)
        
   
class EditScripts:
    def __init__(self,pwindow,savedmap):    
        self.secondclick = None
        self.editbox = None
        self.currentscriptlistbox = None
        y = 0
        
        self.scriptlist =scriptlist = s.cegui.winMgr.createWindow("TaharezLook/Listbox", "scriptlist")
        pwindow.addChildWindow(scriptlist)        
        #scriptlist.setText("actionlist")
        scriptlist.setPosition(CEGUI.UVector2(cegui_reldim(0), cegui_reldim( y)))
        scriptlist.setSize(CEGUI.UVector2(cegui_reldim(1), cegui_reldim( 0.1)))
        scriptlist.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "showScriptList")
        if not savedmap:
            util.addItem(self, scriptlist, "Script1")
            self.scriptmap = dict()
            self.scriptmap["Script1"] = []
        else:
            
            self.scriptmap = savedmap["scriptmap"]
            for x in self.scriptmap.keys():
                util.addItem(self,scriptlist, x)
        self.eventMap = {"Move":data.traits.basictraits.FFTMove(),"FollowCamera": utilities.FollowCamera.FollowCamera()}
        self.eventMap["Move"].range = 50,50
        
        
    def createScript(self,e):
        text =str(self.scriptname.getText())
        util.addItem(self, scriptlist, text)
    def showScriptList(self,e):
        if not e.window.getFirstSelectedItem():
            return
        text = str(e.window.getFirstSelectedItem().getText())
        self.currentscriptlistbox = parent =util.getNewWindow("scripteditlistframe", util.frame, util.rootwindow,.0,.2,.2,.5)
        self.currentscriptlist =scriptlist =util.getNewWindow("scriptlines", util.listbox,parent,0,.1,1,.9)        
        scriptlist.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, "showEditBox")
        for x in self.scriptmap[text]:
            util.addItem(self, scriptlist, str(x))
        util.addItem(self, scriptlist, "Empty")
        self.currentlist = self.scriptmap[text]
        
    def showEditBox(self,e):
        if not e.window.getFirstSelectedItem():
            return
        text = str(e.window.getFirstSelectedItem().getText())
        self.currentEditing = e.window.getFirstSelectedItem()
        self.editbox =parent =util.getNewWindow("scriptframe", util.frame, util.rootwindow,.2,.2,.5,.5)
        util.getNewWindow("unitlistlabelchat", util.statictext,parent,0,.4,.2,.1).setText("unit1")
        self.unit1=util.getNewWindow("chatunitlist", util.combobox,parent,0,.5,.2,.2)
        if self.unit1.getItemCount() == 0:
            first = None
            for x in s.editgame.editunits.unitmap.keys():
                util.addItem(self, self.unit1, x)
                if not first:
                    first = x
            self.unit1.setText(x)
            
       
        self.chattext =util.getNewWindow("chattext", util.multieditbox, parent,.2,.1,.6,.4)
        self.chattext.setText("script text here")
        self.chattime =util.getNewWindow("chattime", util.editbox, parent,.8,.1,.2,.1)
        self.chattime.setText("4")
        btn =util.getNewWindow("chatbtn", util.button, parent,.8,.2,.2,.1)
        btn.setText("addChat")
        btn.subscribeEvent(CEGUI.PushButton.EventClicked, self, "addChat")
        
        util.getNewWindow("unitlistlabel", util.statictext, parent,.2, .6, .2, .1).setText("eventlist")
        self.eventlist=util.getNewWindow("eventlist", util.combobox,parent,.2,.7,.4,.4)
        self.eventlist.subscribeEvent(CEGUI.Combobox.EventTextSelectionChanged, self, "setupEventOptions")
        
        btn =util.getNewWindow("objectbtn", util.button, parent,.8,.8,.2,.1)
        btn.setText("addObject")
        btn.subscribeEvent(CEGUI.PushButton.EventClicked, self, "addObject")
        for x in self.eventMap.keys():
            util.addItem(self, self.eventlist, x)
        #util.getNewWindow("time, type, winname)
        
    def setupEventOptions(self,e):
        if not e.window.getSelectedItem():
            return
        text = str(e.window.getSelectedItem().getText())
        event =self.eventMap[text]
        if event.needsasecondclick:
            if event.unittargeting:
                self.unit2=util.getNewWindow("objunitlist", util.combobox,parent,.4,.7,.2,.2)
            else:
                self.secondclick =util.getNewWindow("secondclick", util.statictext,self.editbox ,.6, .7,.3, .1)
                self.secondclick.setText("Click on map")
                
    def addChat(self,e):
        tuple = (str(self.unit1.getText()),
                 str(self.chattext.getText()),
                 int(str(self.chattime.getText())))
        self.currentlist.append(tuple)
        util.addItem(self,self.currentscriptlist,str(tuple),self.currentscriptlist.getItemCount()-1)
        
    def addObject(self,e):
        
        name = str(self.eventlist.getText())
        event =copy.copy(self.eventMap[name])
        self.currentlist.append(event)
        event.unit1 = str(self.unit1.getText())
        #need to add unit 2
        if event.needsasecondclick:
            if event.unittargeting:
                event.unit1 = str(self.unit1.getText())
            else:
                event.endPos = str(self.secondclick.getText())
        #add extra to signify specific items
        util.addItem(self,self.currentscriptlist,name,self.currentscriptlist.getItemCount()-1)        
    def clickEntity(self,name,position,id,evt):
        if self.secondclick:
            self.secondclick.setText(str(position))
            self.secondclickposition = position
        pass
    
    def close(self):
        #self.secondclick = None
        if self.editbox:
            self.editbox.setVisible(False)
            
        if self.currentscriptlistbox:
            self.currentscriptlistbox.setVisible(False)
    def open(self):
        if self.editbox:
            self.editbox.setVisible(True)
            
        if self.currentscriptlistbox:
            self.currentscriptlistbox.setVisible(True)
    
class EditMeshes:
    def __init__(self,pwindow,savedmap):    
            
        y = 0
        self.selectedmeshes =tex = util.getNewWindow("selectedmesh", "TaharezLook/StaticText")
        tex.setText("")
        tex.setPosition(CEGUI.UVector2(cegui_reldim(0), cegui_reldim(y)))
        tex.setSize(CEGUI.UVector2(cegui_reldim(1), cegui_reldim(0.08)))
        pwindow.addChildWindow(tex)
        
        y += .1
        self.meshesname =eb = s.cegui.winMgr.createWindow("TaharezLook/Editbox", "meshesname")
        pwindow.addChildWindow(eb)
        eb.setPosition(CEGUI.UVector2(cegui_reldim(0.0), cegui_reldim( y)))
        #eb.setMaxSize(CEGUI.UVector2(cegui_reldim(1.0), cegui_reldim( 0.04)))
        eb.setSize(CEGUI.UVector2(cegui_reldim(0.50), cegui_reldim( 0.08)))
        eb.setText("namehere")
        tex = util.getNewWindow("meshesnamedesc", "TaharezLook/StaticText")
        tex.setText("meshesName")
        tex.setPosition(CEGUI.UVector2(cegui_reldim(.5), cegui_reldim(y)))
        tex.setSize(CEGUI.UVector2(cegui_reldim(.5), cegui_reldim(0.08)))
        pwindow.addChildWindow(tex)
        
        y += .1
        self.meshestype =meshestypes = s.cegui.winMgr.createWindow("TaharezLook/Combobox", "meshestypes")
        pwindow.addChildWindow(meshestypes)        
        #meshestypes.setText("actionlist")
        meshestypes.setPosition(CEGUI.UVector2(cegui_reldim(0), cegui_reldim( y)))
        meshestypes.setSize(CEGUI.UVector2(cegui_reldim(1), cegui_reldim( 0.1)))
        
        util.addItem(self, meshestypes, "box")
        util.addItem(self, meshestypes, "ellipsoid")
        
        meshestypes.setText("box")
        
        
        y += .1
        self.meshesscale =eb = s.cegui.winMgr.createWindow("TaharezLook/Editbox", "scale")
        pwindow.addChildWindow(eb)
        eb.setPosition(CEGUI.UVector2(cegui_reldim(0.0), cegui_reldim( y)))
        #eb.setMaxSize(CEGUI.UVector2(cegui_reldim(1.0), cegui_reldim( 0.04)))
        eb.setSize(CEGUI.UVector2(cegui_reldim(0.50), cegui_reldim( 0.08)))
        eb.setText("1")
        
        tex = util.getNewWindow("scaledesc", "TaharezLook/StaticText")
        tex.setText("scale")
        tex.setPosition(CEGUI.UVector2(cegui_reldim(.5), cegui_reldim(y)))
        tex.setSize(CEGUI.UVector2(cegui_reldim(.5), cegui_reldim(0.08)))
        pwindow.addChildWindow(tex)
         
        y +=.1
        btn = CEGUI.WindowManager.getSingleton().createWindow("TaharezLook/Button", "createmeshes")
        pwindow.addChildWindow(btn)
        btn.setText("Create")
        btn.setPosition(CEGUI.UVector2(cegui_reldim(0.2), cegui_reldim(y)))
        btn.setSize(CEGUI.UVector2(cegui_reldim(0.5), cegui_reldim( .1)))
        btn.subscribeEvent(CEGUI.PushButton.EventClicked, self, "createmeshes")  
        
        y += .1
        if savedmap and savedmap.has_key("meshesmap"):
            self.meshesmap = savedmap["meshesmap"]
            self.positionmap = savedmap["positionmap"]
        else:
            self.meshesmap = dict()
            self.meshesmap["dummy"] = tactics.Building.Building()
            
            self.positionmap = dict()
            self.positionmap["dummy"] = (0,0,0) 
        for name in self.meshesmap.keys():
            position =self.positionmap[name]
            tactics.util.showBuilding(self.meshesmap[name],position)
        self.mesheslist = mesheslist = s.cegui.winMgr.createWindow("TaharezLook/Combobox", "mesheslist")
        pwindow.addChildWindow(mesheslist)        
        #mesheslist.setText("actionlist")
        mesheslist.setPosition(CEGUI.UVector2(cegui_reldim(0), cegui_reldim( y)))
        mesheslist.setSize(CEGUI.UVector2(cegui_reldim(1), cegui_reldim( 0.2)))
        for x in self.meshesmap.keys():
            util.addItem(self, mesheslist, x)
        mesheslist.subscribeEvent(CEGUI.Combobox.EventTextSelectionChanged, self, "setCurrentName")


        
        
    def setCurrentName(self,e):
        if not e.window.getSelectedItem():
            return
        text = str(e.window.getSelectedItem().getText())
        item =e.window.getSelectedItem()
        self.selectedmeshes.setText(text)
        
    def createmeshes(self,e):
        text =str(self.meshesname.getText())
        type = str(self.meshestype.getText())
        scale = int(str(self.meshesscale.getText()))
        
        util.addItem(self, self.mesheslist, text)
        self.meshesmap[text] =tactics.Building.Building()
        self.selectedmeshes.setText(text)
        
    def clickEntity(self,name,position,id,evt):
        name = str(self.selectedmeshes.getText())
        if not self.meshesmap.has_key(name):
            return True
        self.positionmap[name] = (position.x,position.y,position.z)
        tactics.util.showBuilding(self.meshesmap[name], position)