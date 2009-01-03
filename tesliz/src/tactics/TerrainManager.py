
#import sys
#sys.path.insert(0,'..')
#import PythonOgreConfig

import ogre.renderer.OGRE as Ogre
import ogre.addons.et as ET
import ogre.io.OIS as OIS
import ogre.gui.CEGUI as CEGUI
#import SampleFramework
import exceptions, random, os
#from CEGUI_framework import *   ## we need the OIS version of the framelistener etc
import ogre.physics.OgreNewt as OgreNewt
### You may have to include this, it causes a problem for me with 
### the way I load CEGUI 
### -
##import os

from tactics.Singleton import *




class TerrainManager:
    mediadir    = "media/ET/"
    def __init__(self):
        self.terrainMgr =  ET.TerrainManager(s.app.sceneManager)
        self.terrainMgr.setLODErrorMargin(2, s.app.camera.getViewport().getActualHeight())
        self.terrainMgr.setUseLODMorphing(True, 0.2, "morphFactor")
        #self.terrainMgr = terrainMgr
        self.splatMgr = ET.SplattingManager("ETSplatting", "ET", 32, 32, 3)
        ## specify number of splatting textures we need to handle
        self.splatMgr.setNumTextures(6)
        s.terrainmanager =self
        
        #self.mRaySceneQuery = self.mSceneMgr.createRayQuery( Ogre.Ray() )

        ## Create a "pointer" for use on the terrain
        #pointer = self.mSceneMgr.createEntity("Pointer", "Ogrehead.mesh")
        #self.mPointer = self.mSceneMgr.getRootSceneNode().createChildSceneNode()
        #self.mPointer.attachObject(pointer)


        ## ETM brush
        self.brushSize = 5
        self.mEditBrush = None
        self.mDeform = True
        self.mChosenTexture = 0
       # self.updateBrush()
        
        s.app.sceneManager.ambientLight = Ogre.ColourValue(0.5, 0.5, 0.5)
        heightMapValues = Ogre.LodDistanceList() ## ET.stdVectorFloat()
        for i in xrange(33):
            for j in xrange(33):
                heightMapValues.append(float(0.50))
        terrainInfo  =ET.TerrainInfo (33, 33, heightMapValues )

        ## save typing self
        
        sceneManager = s.app.sceneManager
        terrainMgr   = self.terrainMgr

        ## set position and size of the terrain
        terrainInfo.setExtents(Ogre.AxisAlignedBox(-50, -50, 0, 1000, 10, 100))
        ## now render it
        terrainMgr.createTerrain(terrainInfo)

        ## create the splatting manager
        self.splatMgr = ET.SplattingManager("ETSplatting", "ET", 32, 32, 3)
        ## specify number of splatting textures we need to handle
        self.splatMgr.setNumTextures(6)

        ## create a manual lightmap texture
        lightmapTex = Ogre.TextureManager.getSingleton().createManual(
        "ETLightmap", "ET", Ogre.TEX_TYPE_2D, 32, 32, 1, Ogre.PF_BYTE_RGB)

        lightmap = Ogre.Image()
        ET.createTerrainLightmap(terrainInfo, lightmap, 32, 32,\
                                 Ogre.Vector3(1, -1, 1),\
                                 Ogre.ColourValue().White,\
                                 Ogre.ColourValue(0.3, 0.3, 0.3,1.0))
        lightmapTex.getBuffer(0, 0).blitFromMemory(lightmap.getPixelBox(0, 0))

        ##  load the terrain material and assign it
        material = Ogre.MaterialManager.getSingleton().getByName("ETTerrainMaterial")
        self.terrainMgr.setMaterial(material)

        ## create terrain manager

#    def updateBrush(self):
#        if not self.mEditBrush is None:
#            self.mEditBrush = None
#        image = Ogre.Image()
#        image.load("brush.png", "ET")
#        image.resize(self.brushSize, self.brushSize)
#        self.mEditBrush = ET.loadBrushFromImage(image)

        ## camera
    map = dict()
    def loadTerrain(self,name):
        #return
        ## destroy current terrain
        self.terrainMgr.destroyTerrain()
        if not self.map.has_key("ET"+name):
            Ogre.ResourceGroupManager.getSingleton().addResourceLocation(
                s.campaigndir + name+"/", "FileSystem", "ET"+name);
        self.map["ET"+name] = "blah"
        ## load terrain map
        image = Ogre.Image()
        image.load("ETterrain.png", "ET"+name)
        info = ET.TerrainInfo()
        
        ET.loadHeightmapFromImage(info, image)
        width = (image.getWidth()-1)/2
        height = (image.getHeight()-1)/2
        info.setExtents(Ogre.AxisAlignedBox(-width, 0, -height, width, 10, height))
        self.terrainMgr.createTerrain(info)
        

        ## load splatting maps
        for i in xrange(self.splatMgr.getNumMaps()):
            filename = "ETcoverage.%s.%s" %( str(i), "png" )
            print "Loading Splatting Map %s " %filename
            image.load( filename , "ET"+name)
            self.splatMgr.loadMapFromImage(i, image)

        ## update lightmap
        self.updateLightmap()
        #self.generateTerrainCollision()
        
    def saveTerrain(self, name):

        ### There is a bug somewhere in the code, I should be able to use
        ### self.getTerrainInfo() but the data isn't there  
        ## check data array
        ##for j in xrange(self.getTerrainInfo().getHeight()):
        ##    for i in xrange(self.getTerrainInfo().getWidth()):
        ##        if self.getTerrainInfo().at(i, j)>0.5:
        ##             print self.getTerrainInfo().at(i, j)

        path =s.campaigndir + name+"/"

        ## save terrain map 
        image = Ogre.Image()
        ET.saveHeightmapToImage(self.getTerrainInfo(), image)
        image.save( os.path.join(path, "ETterrain.png" ))

        ## save the splatting maps
        for i in xrange(self.splatMgr.getNumMaps()):
            self.splatMgr.saveMapToImage(i, image)
            filename = os.path.join(path,"ETcoverage.%s.%s" % ( str(i) , "png")  )
            print "Saving Splatting Map %s " %filename
            image.save( filename )

        ## save light map
        lightmap = Ogre.Image()
        ET.createTerrainLightmap(
                             self.getTerrainInfo() ,
                             lightmap, 64, 64 ,
                             Ogre.Vector3(1, -1, 1) ,
                             Ogre.ColourValue(1 ,1, 1) ,      
                             Ogre.ColourValue(1, 1,  1) )

        lightmap.save(os.path.join(path,"ETlightmap.png") )


        ## generate a base texture for this terrain (could be used for older hardware instead of splatting)
        textures = []
        for i in range(6): 
            image = Ogre.Image()
            textures.append(image)
            
            textures[i].load("splatting%s.%s" %( str(i), "png" ) , "ET")
        ## create the base texture
        baseTexture = Ogre.Image()
        self.splatMgr.createBaseTexture(baseTexture, 64, 64, textures, 20, 20)
        baseTexture.save(os.path.join(path,"ETbase.png"))

        ## finally create a minimap using the lightmap and the generated base texture
        minimap = ET.createMinimap(baseTexture, lightmap)
        print "Saving MinMap to ", os.path.join(path,"ETminimap.png")
        minimap.save(os.path.join(path+"ETminimap.png"))





    def updateLightmap(self):
        ## HACK

        lightmap = Ogre.Image()
        ET.createTerrainLightmap(
                             self.getTerrainInfo() ,
                             lightmap, 32, 32 ,
                             Ogre.Vector3(1, -1, 1) ,
                             Ogre.ColourValue(1 ,1, 1) ,      
                             Ogre.ColourValue(0.3, 0.3,  0.3) )

        ## get our dynamic texture and update its contents
        tex = Ogre.TextureManager.getSingleton().getByName("ETLightmap")
        if not tex:
            return
        l = lightmap.getPixelBox(0, 0)
        tex.getBuffer(0, 0).blitFromMemory(lightmap.getPixelBox(0, 0))
    
    def getTerrainInfo(self):
        return self.terrainMgr.getTerrainInfo()
        
    def getTerrainVertex(self,x,z):

        res =Ogre.Vector3()
       
        res.x = self.getTerrainInfo().getOffset().x + self.getTerrainInfo().getScaling().x * x;
        res.y = self.getTerrainInfo().getOffset().y + self.getTerrainInfo().at(x,z) * self.getTerrainInfo().getScaling().y;
    
        res.z = self.getTerrainInfo().getOffset().z + self.getTerrainInfo().getScaling().z * z;
        return res;

    def generateTerrainCollision(self):
  
        col = OgreNewt.TreeCollision(s.app.World);
        col.start();
        for x in range(0,self.getTerrainInfo().getWidth()-1 ):
            for z in range(0,self.getTerrainInfo().getHeight()-1 ):
                
                v1 = self.getTerrainVertex(x,z);
                v2 = self.getTerrainVertex(x+1,z);
                v3 = self.getTerrainVertex(x+1,z+1);
                v4 = self.getTerrainVertex(x,z+1);
                poly_verts = [0,1,2]
                 
                poly_verts[2] = v1;
                poly_verts[1] = v2;
                poly_verts[0] = v4;
    
                col.addPoly( poly_verts, 0 );
                poly_verts[2] = v2;
                poly_verts[1] = v3;
                poly_verts[0] = v4;
    
                col.addPoly( poly_verts, 0 );
         
        col.finish(False);
       
        self.terrainBody = OgreNewt.Body(s.app.World,col);
        #bod.attachToNode( node )
        #bod.setPositionOrientation( node.getPosition(),node.getOrientation() )        
        
        #terrainBody.attachToNode(s.app.sceneManager.getRootSceneNode())
        

def setupOnlyEvents(filename):
    module = __import__("data.maps."+filename)
    module = getattr(module,'maps')
    map = getattr(module,filename).Unitdata()
    map.setupEvents()
def setupTest(filename):
    try:
        module = __import__("data.maps."+filename)
        module = getattr(module,'maps')
        map = getattr(module,filename).Unitdata()
        map.setupTestMap()
    except Exception,e:
        print e
    
    