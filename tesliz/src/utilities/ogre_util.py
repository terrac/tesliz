# -*- coding: utf-8 -*-

'''Common utility functions for Python-Ogre.
'''
__author__ = 'Ethan Kennerly'

import ogre.renderer.OGRE as ogre 
import ogre_unit

# Disable entity for unit test without rendering.
entity_enabled = True
# Prefabricated cube and sphere have large scale.
PT_SCALE = 100.0




def is_number(value):
    '''
    >>> is_number(None)
    False
    >>> is_number(1)
    True
    >>> is_number(1.1)
    True
    >>> is_number('a')
    False
    '''
    return value is not None and (type(value) is float or type(value) is int)


def xyz(vector):
    '''Conveniently get vector attributes (x, y, z).
    >>> xyz(ogre.Vector3.ZERO)
    (0.0, 0.0, 0.0)
    '''
    if vector:
        return vector.x, vector.y, vector.z
    else:
        return None


def x(vector, x):
    '''Python-Ogre x,y,z attributes do not respond to assignment.
    >>> x(ogre.Vector3(), 1)
    (1.0, 0.0, 0.0)
    >>> x(ogre.Vector3(), '1')
    >>> x(ogre.Vector3(), None)
    '''
    if vector:
        if is_number(x):
            return (float(x), vector.y, vector.z)


def y(vector, y):
    if vector:
        if is_number(y):
            return (vector.x, float(y), vector.z)


def z(vector, z):
    if vector:
        if is_number(z):
            return (vector.x, vector.y, float(z))


# TODO:  Fix gimball lock or other rotation corruption cases.
def set_yaw(node, yaw):
    if node:
        if is_number(yaw):
            relative_yaw = ogre.Radian(yaw) - node.orientation.getYaw()
            node.yaw(relative_yaw)


def set_pitch(node, pitch):
    if node:
        if is_number(pitch):
            relative_pitch = ogre.Radian(pitch) - node.orientation.getPitch()
            node.pitch(relative_pitch)


def set_roll(node, roll):
    if node:
        if is_number(roll):
            relative_roll = ogre.Radian(roll) - node.orientation.getRoll()
            node.roll(relative_roll)


def setMaterial(node, materialName):
    '''Set material for every entity's sub entity.
        >>> application = ogre_unit.setup_unittest_application()
        >>> sceneManager = application.sceneManager
        >>> node = create_object(sceneManager, 'ba', None)
        >>> setMaterial(node, 'Examples/Hilite/Yellow')
    '''
    object_iterator = node.getAttachedObjectIterator()
    while object_iterator.hasMoreElements():
        entity = object_iterator.getNext()
        if hasattr(entity, 'getNumSubEntities'):
            for s in range(entity.getNumSubEntities()):
                sub = entity.getSubEntity(s)
                sub.materialName = materialName


def reload_mesh(node):
    '''Reload mesh from file for each top-level entity.'''
    object_iterator = node.getAttachedObjectIterator()
    while object_iterator.hasMoreElements():
        entity = object_iterator.getNext()
        if hasattr(entity, 'mesh'):
            object.mesh.reload()


def create_object(sceneManager, name, mesh, materialName=None, parent_node=
        None):
    '''Create scene node and entity.  Return node.'''
    if not parent_node:
        node = sceneManager.rootSceneNode.createChildSceneNode(name)
    else:
        node = parent_node.createChildSceneNode(name)
    if mesh and entity_enabled:
        entity = sceneManager.createEntity(name, mesh)
        if materialName:
            sub = entity.getSubEntity(0)
            sub.materialName = materialName
        node.attachObject(entity)
    return node


def create_cube(sceneManager, name, scale=1):
    node = ogre_util.create_object(sceneManager, name, sceneManager.PT_CUBE)
    global PT_SCALE
    node.scale = (scale / PT_SCALE, scale / PT_SCALE, scale / PT_SCALE)
    return node


def set_tree_visible(sceneManager, root_node, is_visible):
    if sceneManager.hasSceneNode(root_node.name):
        iterator = root_node.getChildIterator()
        while iterator.hasMoreElements():
            child = iterator.getNext()
            child.setVisible(is_visible)
        root_node.setVisible(is_visible)    
    else:
        print '! set_tree_visible: node not found:', root_node, sceneManager


def destroy_structure(sceneManager, node):
    '''Destroy node, entities, and child nodes.'''
    if sceneManager.hasSceneNode(node.name):
        iterator = node.getChildIterator()
        while iterator.hasMoreElements():
            child = iterator.getNext()
            entity_iterator = child.getAttachedObjectIterator()
            while entity_iterator.hasMoreElements():
                entity = entity_iterator.getNext()
                sceneManager.destroyEntity(entity.name)
            sceneManager.destroySceneNode(child.name)
        entity_iterator = node.getAttachedObjectIterator()
        while entity_iterator.hasMoreElements():
            entity = entity_iterator.getNext()
            sceneManager.destroyEntity(entity.name)
        sceneManager.destroySceneNode(node.name)
    else:
        print '! destroy_object: node not found:', node, sceneManager


def child_name_list(ogre_scene_node, name_list):
    '''Return a sorted list of child node names of an Ogre scene node.
    >>> application = ogre_unit.setup_unittest_application()
    >>> root_node = application.sceneManager.getRootSceneNode()
    >>> root_node.name
    'root node'
    >>> child = root_node.createChildSceneNode('child_node')
    >>> child_name_list( root_node, [] )
    ['root node', 'child_node']
    >>> grandchild = child.createChildSceneNode('grandchild_node')
    >>> name_list = child_name_list( root_node, [] )
    >>> name_list
    ['root node', 'child_node', 'grandchild_node']
    '''
    if ogre_scene_node:
        name_list.append(ogre_scene_node.name)
        node_iterator = ogre_scene_node.getChildIterator()
        while node_iterator.hasMoreElements():
            node = node_iterator.getNext()
            child_list = child_name_list(node, name_list)
            if child_list:  
                if 1 == len(child_list):
                    name_list.append(child_list)
        return name_list


def sorted_child_name_list(ogre_scene_node):
    '''Return self and child names, sorted by name.'''
    name_list = child_name_list(ogre_scene_node, [])
    name_list.sort()
    return name_list


def create_grid(sceneManager, spacing, lower_bound=None, upper_bound=None):
    '''2D grid of markers about the origin (0,0,0) for detecting motion.
    Every 5th and 10th is larger.  spacing should be integer 1 or greater.
    '''
    assert 1 <= spacing
    if sceneManager.hasSceneNode('grid'):
        print 'grid exists'
        destroy_structure(sceneManager, sceneManager.getSceneNode('grid'))
    
    grid_parent_node = sceneManager.rootSceneNode.createChildSceneNode(
        'grid')
    base_markerScale = 0.001 * spacing
    radius = 5 * spacing
    if lower_bound is None and upper_bound is None:
        lower_bound = - radius, - radius
        upper_bound = radius, radius
    index = 0
    for x in range(lower_bound[0], upper_bound[0], int(spacing)):
        for z in range(lower_bound[1], upper_bound[1], int(spacing)):
            markerEnt = sceneManager.createEntity(
                'grid_' + str(index), sceneManager.PT_CUBE)
            index += 1
            markerScale = base_markerScale
            if (x / spacing) % 10 == 0 and (z / spacing) % 10 == 0:
                markerScale = base_markerScale * 4
            elif (x / spacing) % 5 == 0 and (z / spacing) % 5 == 0:
                markerScale = base_markerScale * 2
            localMarkerNode = grid_parent_node.createChildSceneNode(
                'grid_' + str(index), (x, 0, z))
            localMarkerNode.attachObject(markerEnt)
            localMarkerNode.setScale(
                markerScale, markerScale, markerScale)


def camera_orbit(camera, (dx, dy, dz), (tx, ty, tz)):
    '''Move while looking at target.  Return new position.
        >>> application = ogre_unit.setup_unittest_application()
        >>> camera = application.camera
        >>> camera.position = (2.0, 7.0, 5.0)
        >>> camera_orbit(camera, (0.5,0.5,0), (2.5,0,2.5))
        (2.5, 7.5, 5.0)
    '''
    camera.move(ogre.Vector3(dx, dy, dz))
    camera.lookAt(tx, ty, tz)
    return camera.position.x, camera.position.y, camera.position.z
            

def attach_camera(camera, node):
    '''Move node to camera and inherit camera position from node.'''
    camera_node.position = camera.position
    camera_node.orientation = camera.orientation
    camera.position = ogre.Vector3.ZERO
    camera.orientation = ogre.Quaternion()
    camera_node.attachObject(camera)
    return camera_node


def attach_camera_to_node(sceneManager, camera, camera_node_name='Camera'):
    '''Camera is relative to node, which can be moved conveniently.'''
    camera_node = sceneManager.createSceneNode(camera_node_name)
    return attach_camera(camera, camera_node)


if __name__ == '__main__':
    import code_util
    code_util.test(__file__)
