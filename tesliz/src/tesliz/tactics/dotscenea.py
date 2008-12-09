#!/usr/bin/python
"""
this file parses .scene node (dotscene) files and
creates them in OGRE with user data

Doesn't do any fancy stuff (skydome, XODE, lightmapping, etc) but you can use this as a base for adding those features.)

cpp:
http://www.ogre3d.org/wiki/index.php/DotScene_Loader_with_User_Data_Class
"""
from xml.dom import minidom, Node
import ogre.renderer.OGRE as Ogre
import utilities.ogre_unit
import utilities.ogre_util
import ogre.physics.OgreNewt as OgreNewt
from tactics.Singleton import *
import tactics.Unit 



'''
Adapted from:
python / /www.Ogre3d.org/phpBB2addons/viewtopic.php?t=1583

Using 'quaternion' and 'qw' as in Blender Scene Exporter.
https://svn.Ogre3d.org/svnroot/Ogreaddons/trunk/blendersceneexporter/

Python-Ogre 1.1 dotscene.py demo uses 'rotation' and 'qw' ...'qz' whereas Blender Dot Scene exporter uses 'quaternion' and 'w'...'z'.  Which one is the current 'standard'?  The documentation is conflicting.  It is 'qw' and 'rotation' here:
http://www.Ogre3d.org/wiki/index.php/DotScene
http://www.Ogre3d.org/wiki/index.php/New_DotScene_Loader
'''


# Contrive power of 1/2 for test data.
unit_test_xml_string = u'''<?xml version="1.0" ?><scene formatVersion="1.0.0">
  <nodes>
    <node name="testscene_cube">
      <position x="0.000000" y="0.000000" z="0.000000"/>
      <quaternion w="1.000000" x="0.000000" y="0.000000" z="0.000000"/>
      <scale x="1.000000" y="1.000000" z="1.000000"/>
    </node>
    <node name="Camera">
      <position x="7.0" y="5.0" z="6.0"/>
      <quaternion w="0.875" x="-0.25" y="0.375" z="0.0625"/>
      <scale x="1.000000" y="1.000000" z="1.000000"/>
      <camera fov="38.0" name="Camera" projectionType="perspective">
        <clipping farPlaneDist="100.000000" nearPlaneDist="0.100000"/>
      </camera>
    </node>
  </nodes>
  <environment>
    <colourAmbient b="0.000000" g="0.000000" r="0.000000"/>
    <colourBackground b="0.400000" g="0.220815" r="0.056563"/>
  </environment>
</scene>'''

user_test_xml_string = u'''<?xml version="1.0" ?><scene formatVersion="1.0.0">
  <nodes>
    <node name="testscene_cube">
      <position x="0.000000" y="0.000000" z="0.000000"/>
      <quaternion w="1.000000" x="0.000000" y="0.000000" z="0.000000"/>
      <scale x="1.000000" y="1.000000" z="1.000000"/>
      <entity meshFile="testscene_cube_mesh.mesh" name="testscene_cube"/>
    </node>
    <node name="Camera">
      <position x="7.481132" y="5.343665" z="6.507640"/>
      <quaternion w="0.893293" x="-0.212056" y="0.386910" z="0.085793"/>
      <scale x="1.000000" y="1.000000" z="1.000000"/>
      <camera fov="37.849289" name="Camera" projectionType="perspective">
        <clipping farPlaneDist="100.000000" nearPlaneDist="0.100000"/>
      </camera>
    </node>
    <node name="Lamp">
      <position x="4.076245" y="5.903862" z="-1.005454"/>
      <quaternion w="0.523275" x="-0.284166" y="0.726942" z="0.342034"/>
      <scale x="1.000000" y="1.000000" z="1.000000"/>
      <light name="Spot" type="point">
        <colourDiffuse b="1.000000" g="1.000000" r="1.000000"/>
        <colourSpecular b="1.000000" g="1.000000" r="1.000000"/>
        <lightAttenuation constant="1.000000" linear="0.033333" quadratic="0.000000" range="5000.0"/>
      </light>
    </node>
  </nodes>
  <externals>
    <item type="material">
      <file name="Scene.material"/>
    </item>
  </externals>
  <environment>
    <colourAmbient b="0.000000" g="0.000000" r="0.000000"/>
    <colourBackground b="0.400000" g="0.220815" r="0.056563"/>
  </environment>
</scene>'''

def get_test_xml():
    '''Setup XML dotscene for parsing.
    >>> xmldoc = get_test_xml()
    '''
    return minidom.parseString(unit_test_xml_string)

def find_nodes(root, name):
    '''Find nodes that are children of root and have the given name.'''
    out=minidom.NodeList()
    if root.hasChildNodes:
        node_list = root.childNodes
        for node in node_list:
            if node.nodeType == Node.ELEMENT_NODE and node.nodeName == name:
                out.append(node)
    return out

def parse_floats(xml_node, object_name, *property_name_list):
    '''Parse properties of xml_node's subnode as floats.
    >>> xml = get_test_xml()
    >>> xml_node_list = xml.getElementsByTagName('node')
    >>> xml_node = xml_node_list[0]
    >>> position = parse_floats(xml_node, 'position', 'x', 'y', 'z')
    >>> assert type(position[2]) == float
    '''
    object = find_nodes(xml_node, object_name)[0].attributes
    property_list = []
    for p in property_name_list:
        property_list.append(float(object[p].nodeValue))
    return tuple(property_list)


def parse_name(xml_node):
    '''Get name if there is one.
    '''
    name = None
    name_attribute = xml_node.attributes.get('name')
    if name_attribute:
        name = str(name_attribute.nodeValue)
    return name


def parse_scene_node(sceneManager, xml_node):
    r'''Create and return scene node from DTD attributes.
    >>> application = Ogre_unit.setup_unittest_application()
    >>> xml = get_test_xml()
    >>> xml_node = xml.getElementsByTagName('node')[0]
    >>> node = parse_scene_node(application.sceneManager, xml_node)
    >>> scene_node_name = xml_node.attributes['name'].nodeValue
    >>> application.sceneManager.hasSceneNode(scene_node_name)
    True
    '''
    name = str(xml_node.attributes['name'].nodeValue)
    if not sceneManager.hasSceneNode(name):
        
        scene_node = sceneManager.getRootSceneNode().createChildSceneNode(name)
    else:
        scene_node = sceneManager.getSceneNode(name)
    scene_node.position = parse_floats(xml_node, 'position', 'x', 'y', 'z')
    try:
        w,x,y,z = parse_floats(xml_node, 'quaternion', 'w', 'x', 'y', 'z')
    except IndexError:
        w,x,y,z = 1,0,0,0
    scene_node.orientation = Ogre.Quaternion(w,x,y,z)
    scene_node.setScale(parse_floats(xml_node, 'scale', 'x', 'y', 'z'))
    return scene_node


def parse_camera(sceneManager, xml_node):
    '''Parse DTD node as camera.  Return camera.
    >>> application = Ogre_unit.setup_unittest_application()
    >>> xml = get_test_xml()

    Gracefully ignore non-camera.
    >>> xml_node = xml.getElementsByTagName('node')[0]
    >>> camera_list = parse_camera(application.sceneManager, xml_node)
    >>> application.sceneManager.hasSceneNode(parse_name(xml_node))
    False

    Parse actual camera.
    >>> xml_node = xml.getElementsByTagName('node')[1]
    >>> camera_list = parse_camera(application.sceneManager, xml_node)
    >>> application.sceneManager.hasSceneNode(parse_name(xml_node))
    True
    >>> camera_list[0].name
    'Camera'
    >>> camera = camera_list[0]

    Camera is oriented and positioned as specified on node.
    >>> camera.isVisible(Ogre.Vector3(0, 0, 0))
    True
    >>> assert camera.orientation == Ogre.Quaternion()
    >>> assert camera.position == Ogre.Vector3.ZERO
    >>> node = camera.getParentSceneNode()
    >>> node.name
    'Camera'
    >>> Ogre_util.xyz(camera.position)
    (0.0, 0.0, 0.0)
    >>> Ogre_util.xyz(camera.orientation)
    (0.0, 0.0, 0.0)
    >>> Ogre_util.xyz(node.position)
    (7.0, 5.0, 6.0)
    >>> Ogre_util.xyz(node.orientation)
    (-0.25, 0.375, 0.0625)
    >>> camera.fOVy.valueDegrees()
    38.0
    '''
    # is it a camera?
    # TODO: there are other attributes I need in here
    camera_xml_nodes = find_nodes(xml_node, 'camera')
    if not camera_xml_nodes:
        return
    camera_list = []
    for camera_xml_node in camera_xml_nodes:
        name = parse_name(camera_xml_node)
        thingy = find_nodes(xml_node, 'camera')[0].attributes
        fov = float(thingy['fov'].nodeValue)
        projectionType= str(thingy['projectionType'].nodeValue)
        # TODO apply general solution to other types.
        scene_node = parse_scene_node(sceneManager, xml_node)
       # if not sceneManager.hasCamera(name):
       #     camera = sceneManager.createCamera(name)
       #     s.app.msnCam = s.app.sceneManager.getRootSceneNode().createChildSceneNode()
       #     s.app.msnCam.attachObject( s.app.camera )
       #     s.app.camera.setPosition(0.0, 0.0, 0.0)
       #     s.app.msnCam.setPosition( scene_node.getPosition())
       # else:
        camera = sceneManager.getCamera(name)
        camera.position = Ogre.Vector3.ZERO
        camera.orientation = Ogre.Quaternion()
        clippings = find_nodes(camera_xml_node, 'clipping')
        if clippings:
            # Could there be more than one 'clipping'?
            clipping = clippings[0]
            camera.nearClipDistance, camera.farClipDistance = parse_floats(
                    camera_xml_node, 'clipping', 'nearPlaneDist', 'farPlaneDist')
        camera.FOVy = Ogre.Degree(fov)
        
        s.app.msnCam.setPosition(scene_node.getPosition())
        s.app.msnCam.setOrientation(scene_node.getOrientation())
        #camera.orientation = scene_node.getOrientation()
        #scene_node.attachObject(camera)
        s.app.sceneManager.destroySceneNode(scene_node)
        camera_list.append(camera)
    return camera_list


def parse_light(sceneManager, xml_node):
    '''Return light with parameters populated by xml_node.'''
    # TODO:  refactor Python-Ogre 1.1 demo light/entity 'dotscene.py' into functions 
    # TODO:  Cleanup style, as in parse_camera.
    scene_node = parse_scene_node(sceneManager, xml_node)
    attachMe = None
    # is it a light?
    try:
        thingy = find_nodes(xml_node, 'light')[0].attributes
        name = str(thingy['name'].nodeValue)
        attachMe = sceneManager.createLight(name)
        ltypes={'point':Ogre.Light.LT_POINT,'directional':Ogre.Light.LT_DIRECTIONAL,'spot':Ogre.Light.LT_SPOTLIGHT,'radPoint':Ogre.Light.LT_POINT}
        try:
            attachMe.type = ltypes[thingy['type'].nodeValue]
        except IndexError:
            pass
        
        lightNode = find_nodes(xml_node, 'light')[0]

        try:
            tempnode = find_nodes(lightNode, 'colourSpecular')[0]
            attachMe.specularColour = (float(tempnode.attributes['r'].nodeValue), float(tempnode.attributes['g'].nodeValue), float(tempnode.attributes['b'].nodeValue), 1.0)
        except IndexError:
            pass
        
        try:
            tempnode = find_nodes(lightNode, 'colourDiffuse')[0]
            attachMe.diffuseColour = (float(tempnode.attributes['r'].nodeValue), float(tempnode.attributes['g'].nodeValue), float(tempnode.attributes['b'].nodeValue), 1.0)
        except IndexError:
            pass
        
        try:
            tempnode = find_nodes(lightNode, 'colourDiffuse')[0]
            attachMe.diffuseColour = (float(tempnode.attributes['r'].nodeValue), float(tempnode.attributes['g'].nodeValue), float(tempnode.attributes['b'].nodeValue), 1.0)
        except IndexError:
            pass
        
        
        scene_node.attachObject(attachMe)
        return attachMe
    except IndexError:
        return


class Dotscene(object):
	
	#playermap = ("Player1",HumanPlayer()),("Computer1",ComputerPlayer())
    s = Singleton()
    
    def parse_entity(self,sceneManager, xml_node):
        '''Return entity with parameters populated by xml_node.'''
        # TODO:  refactor Python-Ogre 1.1 demo light/entity 'dotscene.py' into functions 
        # TODO:  Cleanup style, as in parse_camera.
        # Should scene node also be returned?  Should scene node be factored out?
        scene_node = parse_scene_node(sceneManager, xml_node)
        
        
        
        attachme = None
         
        try:
            thingy = find_nodes(xml_node, 'entity')[0].attributes
            name = str(thingy['name'].nodeValue)
            mesh = str(thingy['meshFile'].nodeValue)
            attachMe = sceneManager.createEntity(name,mesh)
            
            scene_node.attachObject(attachMe)
            #TODO: for later 
          #  attachMe.setMaterialName( "Examples/RustySteel" )
            #attachMe.setNormaliseNormals(True)
            unit = tactics.Unit.Unit(scene_node.getName())
            unit.node = scene_node
            
        
            getattr(self.map, name)(unit)
            

            
        except IndexError:
            return
        return attachMe
        
    
    filename = None    
    def parse_scene(self,sceneManager, xml):
        self.filename = xml
        
        xml =  minidom.parse(xml+'.scene')
        '''Modify and return reference to sceneManager from elements specified in dotscene XML document. 
        >>> application = Ogre_unit.setup_unittest_application()
        >>> xml = get_test_xml()
        >>> application.sceneManager = parse_scene(application.sceneManager, xml)
        '''
        # TODO: check DTD to make sure you get all nodes/attributes
        # TODO: Use the userData for sound/physics
        
        module = __import__("data.maps."+self.filename)
        module = getattr(module,'maps')
        self.map = getattr(module,self.filename).Unitdata()
        
        xml_node_list = xml.getElementsByTagName('node')
        for xml_node in xml_node_list:
            if xml_node.nodeType == Node.ELEMENT_NODE and xml_node.nodeName == 'node': 
                camera = parse_camera(sceneManager, xml_node)
                light = parse_light(sceneManager, xml_node)
                entity = self.parse_entity(sceneManager, xml_node)
                
        
        self.map.setupEvents()       
        
                
        return sceneManager 
    
    app = None
     
    def setup_scene(self,sceneManager, xml,papp):
        '''Create scene from XML file and apply defaults.
        >>> application = Ogre_unit.setup_unittest_application()
        >>> xml = get_test_xml()
        >>> application.sceneManager = setup_scene(application.sceneManager, xml)
        '''
        self.app = papp
        sceneManager.setAmbientLight(Ogre.ColourValue(0.2,0.2,0.2))
        sceneManager = self.parse_scene(sceneManager, xml)
        if sceneManager.hasCamera('Camera'):
            camera = sceneManager.getCamera('Camera')
            camera.lookAt(Ogre.Vector3(0, 0, 0))
        return sceneManager
    

def setup_test_dotscene_application(setup_function, xml, application = None):
    '''Test dotscene.  Null root for unit-test.
    >>> application = setup_test_dotscene_application(Ogre_unit.setup_unittest, get_test_xml())
    >>> del application
    '''
    application = Ogre_unit.setup_quiet_application(setup_function, application)
    application.sceneManager = setup_scene(application.sceneManager, xml)
    Ogre_util.create_grid(application.sceneManager, 1, (-10,-10), (10,10))
    return application


#class test_dotscene_application_class(Ogre_unit.application_class):
    '''Test of dotscene loader for an application.
    >>> application = test_dotscene_application_class()

    Need resources for camera, light, entity.  Must startRendering.
    >>> application.go()
    '''
#    def __init__(self):
#        return Ogre_unit.application_class.__init__(self)
#    def go(self):
#        self = Ogre_unit.setup_quiet_application(Ogre_unit.setup, self)
#        self.sceneManager = setup_scene(self.sceneManager, minidom.parse('../model/axis.scene'))
#        Ogre_util.create_grid(self.sceneManager, 1, (-10,-10), (10,10))
#        self.root.startRendering()

def setupOnlyEvents(filename):
    module = __import__("data.maps."+filename)
    module = getattr(module,'maps')
    map = getattr(module,filename).Unitdata()
    map.setupEvents()
def setupTest(filename):
    module = __import__("data.maps."+filename)
    module = getattr(module,'maps')
    map = getattr(module,filename).Unitdata()
    map.setupTestMap()
if __name__ == "__main__":
    import code_util
    code_util.test(__file__)
