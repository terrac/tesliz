import ogre.renderer.OGRE as Ogre
import ogre.addons.et as ET
import ogre.io.OIS as OIS
import ogre.gui.CEGUI as CEGUI
import exceptions, random, os
import ogre.physics.OgreNewt as OgreNewt
from tactics.Singleton import *
import util
import tactics.util
import shelve

class EditGame:
    mapname = "media\\et\\"
    def getMapName(self):
        return self.mapname + self.name +"\\mapdata.dat"
    def __init__(self,name ):
        self.name = name
        
        #destroy and save current layout
        s.cegui.hide()
        s.framelistener.unitqueue.clearUnitQueue()
        s.framelistener.pauseturns = True
        s.framelistener.cplayer =self
        
        savedmap = None
        
        if os.path.exists(self.getMapName()):
            savedmap = shelve.open(self.getMapName())
            
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
        tbc.subscribeEvent(CEGUI.Window.EventMouseClick, self, "setCurrentTab")
        terrain =s.cegui.winMgr.createWindow("DefaultGUISheet", "Terrain")
        terrain.setText("Terrain")
        #tbc.addTab(terrain)
        #self.editterrain = EditTerrain(terrain)
        #self.currentClick = self.editterrain
        
        tab2 =s.cegui.winMgr.createWindow("DefaultGUISheet", "Units")
        tab2.setText("Units")
        tbc.addTab(tab2)
        self.editunits = EditUnits(tab2,savedmap)
        self.currentClick = self.editunits
        
        tab3 =s.cegui.winMgr.createWindow("DefaultGUISheet", "Meshes")
        tab3.setText("Meshes")
        tbc.addTab(tab3)
#        mainMenuBackground.addChildWindow(jobButton)

        btn = util.getNewWindow("save", "TaharezLook/Button", "root_wnd")
        
        btn.setText("save")
        btn.setPosition(CEGUI.UVector2(cegui_reldim(0.835), cegui_reldim( 0.85)))
        btn.setSize(CEGUI.UVector2(cegui_reldim(0.1), cegui_reldim( 0.05)))
        btn.subscribeEvent(CEGUI.PushButton.EventClicked, self, "saveGame")
             
        if savedmap:
            savedmap.close()

    def clickEntity(self,name,position,id,evt):
        self.currentClick.clickEntity(name, position, id, evt)


    def setCurrentTab(self, e):
        
        text = str(e.window.getActiveChild().getText())
        if text == "Terrain":
            self.currentClick = self.editterrain
        if text == "Units":
            self.currentClick = self.editunits
        return True
    def saveGame(self,e):
        s.terrainmanager.saveTerrain(self.name)
        
        savedmap = shelve.open(self.getMapName())
        
        for x in self.editunits.unitmap.values():
            x.node = None
        savedmap["unitmap"] = self.editunits.unitmap
        savedmap["positionmap"] = self.editunits.positionmap
        
        savedmap.close()
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

        
        x = int( s.terrainmanager.terrainInfo.posToVertexX(position.x) )
        z = int( s.terrainmanager.terrainInfo.posToVertexZ(position.z) )
        dr = -1
        
        if ( id == OIS.MB_Left ):
            dr = 1
        intensity = 1 * dr
        if self.deform:
            s.terrainmanager.terrainMgr.deform(x,z, self.mEditBrush,intensity)
        else:
            s.terrainmanager.splatMgr.paint(self.texlist.index(self.texture), x, z, self.mEditBrush, 1)
        #s.terrainmanager.generateTerrainCollision()
class EditUnits:
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
        unittypes.setSize(CEGUI.UVector2(cegui_reldim(1), cegui_reldim( 0.1)))
        
        util.addItem(self, unittypes, "Squire")
        util.addItem(self, unittypes, "Chemist")
        util.addItem(self, unittypes, "Wizard")
        unittypes.setText("Squire")
        
        
        y += .1
        self.unitplayer =unitplayers = s.cegui.winMgr.createWindow("TaharezLook/Combobox", "unitPlayer")
        pwindow.addChildWindow(unitplayers)        
        #unitplayers.setText("actionlist")
        unitplayers.setPosition(CEGUI.UVector2(cegui_reldim(0), cegui_reldim( y)))
        unitplayers.setSize(CEGUI.UVector2(cegui_reldim(1), cegui_reldim( 0.1)))
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
            self.positionmap = dict() 
        for name in self.positionmap.keys():
            position =self.positionmap[name]
            self.showUnit(name,position)
        self.unitlist = unitlist = s.cegui.winMgr.createWindow("TaharezLook/Combobox", "unitlist")
        pwindow.addChildWindow(unitlist)        
        #unitlist.setText("actionlist")
        unitlist.setPosition(CEGUI.UVector2(cegui_reldim(0), cegui_reldim( y)))
        unitlist.setSize(CEGUI.UVector2(cegui_reldim(1), cegui_reldim( 0.2)))
        for x in self.unitmap.keys():
            util.addItem(self, unitlist, x)
        unitlist.subscribeEvent(CEGUI.Combobox.EventTextSelectionChanged, self, "setCurrentName")


        
        
    def setCurrentName(self,e):
        if not e.window.getSelectedItem():
            return
        text = str(e.window.getSelectedItem().getText())
        item =e.window.getSelectedItem()
        self.selectedunit.setText(text)
    def createUnit(self,e):
        text =str(self.unitname.getText())
        type = str(self.unittype.getText())
        level = int(str(self.unitlevel.getText()))
        player = str(self.unitplayer.getText())
        util.addItem(self, self.unitlist, text)
        self.unitmap[text] =tactics.util.buildUnitNoNode(text,player, type,)
        self.selectedunit.setText(text)
        
    def clickEntity(self,name,position,id,evt):
        name = str(self.selectedunit.getText())
        if not self.unitmap.has_key(name):
            return True
        self.positionmap[name] = (position.x,position.y,position.z)
        self.showUnit(name, position)
        
    def showUnit(self, name, position):
        unit = self.unitmap[name]
        sceneManager = s.app.sceneManager
        name = unit.name
        prevhad = False
        if sceneManager.hasSceneNode(name):
            scene_node = sceneManager.getSceneNode(name)
            prevhad = True
        else:
            scene_node = sceneManager.getRootSceneNode().createChildSceneNode(name)
        scene_node.position = position
        if not prevhad:
            if s.app.sceneManager.hasEntity(name):
                attachMe = s.app.sceneManager.getEntity(name)
            else:
                attachMe = sceneManager.createEntity(name, unit.job.mesh)
            scene_node.attachObject(attachMe)
        scene_node.setScale(Ogre.Vector3(1, .5, 1))
        unit.node = scene_node
        if not prevhad:
            tactics.util.buildPhysics(unit)
        #s.unitmap[unit.getName()]=unit
        unit.node.getAttachedObject(0).setMaterialName(unit.job.material)
        #unit.node.getAttachedObject(0).setMaterialName("Examples/RustySteel")
        if hasattr(unit.player, "setVisualMarker"):
            unit.player.setVisualMarker(unit)

        