#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Simple Python-Ogre application functions.
Derived from SampleFramework, reimplemented as a toolkit for agile prototyping or succinct unit-testing.  Assemble an application from the functions.
'''
__author__ = 'Ethan Kennerly'

import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import code_util


def getPluginPath():
    """Return the absolute path to a valid plugins.cfg file.
    Copied from sf_OIS.py""" 
    import sys
    import os
    import os.path
    
    paths = [os.path.join(os.getcwd(), 'plugins.cfg'),
             '/etc/OGRE/plugins.cfg',
             os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'plugins.cfg')]
    for path in paths:
        if os.path.exists(path):
            return path

    sys.stderr.write("\n"
        "** Warning: Unable to locate a suitable plugins.cfg file.\n"
        "** Warning: Please check your ogre installation and copy a\n"
        "** Warning: working plugins.cfg file to the current directory.\n\n")
    raise ogre.Exception(0, "can't locate the 'plugins.cfg' file", "")


def setup_resources(resources_path = 'resources.cfg'):
    '''Load resources, such as from 'resources.cfg'.'''
    config = ogre.ConfigFile()
    config.load(resources_path)
    section_iter = config.getSectionIterator()
    while section_iter.hasMoreElements():
        section_name = section_iter.peekNextKey()
        settings = section_iter.getNext()
        for item in settings:
            ogre.ResourceGroupManager.getSingleton().addResourceLocation(item.value, item.key, section_name)


def setup_root(plugins_path = getPluginPath(), 
        resources_path = 'resources.cfg'):
    '''Return new root, sceneManager.'''
    root = ogre.Root(plugins_path)
    root.setFrameSmoothingPeriod(5.0)
    setup_resources(resources_path)
    sceneManager = root.createSceneManager(ogre.ST_GENERIC,"ExampleSMInstance")
    return root, sceneManager


def initialise_null_render(plugins_path = getPluginPath()): 
    'Prepare to null renderer and return ogre root.'
    ogre_root = ogre.Root(plugins_path)
    rend_list = ogre_root.getAvailableRenderers()
    ogre_root.setRenderSystem(rend_list[-1])
    ogre_root.getRenderSystem()._initRenderTargets()
    ogre_root.initialise(False)
    return ogre_root


def setup_null_root(plugins_path = getPluginPath(), 
        resources_path = 'resources.cfg'):
    '''Return root, sceneManager.  Suitable for unit test without entity, camera, light.
    >>> logManager, logListener = quiet_log()
    >>> root, sceneManager = setup_null_root()
    >>> assert root
    >>> assert sceneManager
    >>> for i in range(10):
    ...     if not renderOneFrame(root):  print False
    >>> del sceneManager, root
    >>> del logManager, logListener
    '''
    root = initialise_null_render(plugins_path)
    setup_resources(resources_path)
    sceneManager = root.createSceneManager(ogre.ST_GENERIC,"ExampleSMInstance")
    return root, sceneManager


def setup_viewport(root, sceneManager):
    '''Create render window and viewport from user selection, and return renderWindow and camera.'''
    renderWindow = configure(root)
    if not renderWindow:
        return None
    camera = sceneManager.createCamera('Camera')
    viewport = renderWindow.addViewport(camera)
    return renderWindow, camera


def configure(ogre_root):
    """This shows the config dialog and returns the renderWindow."""
    user_confirmation = ogre_root.showConfigDialog()
    if user_confirmation:
        return ogre_root.initialise(True, "OGRE Render Window")
    else:
        return None


def setup_unittest():
    '''With tiny render window and resources.  Return root and sceneManager.
    >>> logManager, logListener = quiet_log()
    >>> root, sceneManager, renderWindow, camera = setup_unittest()
    >>> assert root
    >>> assert sceneManager
    >>> assert renderWindow
    >>> assert camera
    >>> del sceneManager, root, renderWindow, camera
    >>> del logManager, logListener
    '''
    root, sceneManager = setup_null_root()
    renderWindow = root.createRenderWindow('test', 4, 3, False)
    camera = sceneManager.createCamera('Camera')
    ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()
    return root, sceneManager, renderWindow, camera


def setup():
    '''Set up minimal Ogre application and return root and sceneManager.
    >>> logManager, logListener = quiet_log()
    
    # TODO:  Doctest crashes, although external call to setup works!
    #>>> root, sceneManager, renderWindow, camera = setup()
    #>>> assert root
    #>>> assert sceneManager
    #>>> assert renderWindow
    #>>> assert camera
    #>>> application = setup_quiet_application(setup_unittest)
    #>>> for i in range(10):
    #...     print i,
    #...     if not renderOneFrame(root):  print False
    #0 1 2 3 4 5 6 7 8 9
    #>>> sceneManager.clearScene()

    #>>> del renderWindow
    #>>> del camera
    #>>> del sceneManager
    #>>> del root
    >>> del logManager, logListener
    '''
    root, sceneManager = setup_root()
    renderWindow, camera = setup_viewport(root, sceneManager)
    ogre.TextureManager.getSingleton().setDefaultNumMipmaps(5)
    ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()
    return root, sceneManager, renderWindow, camera


def run(root, sceneManager, renderWindow, camera):
    '''Construct and render.'''
    root, sceneManager, renderWindow, camera = setup()
    if root and sceneManager:
        root.startRendering()


def renderOneFrame(ogre_root):
    'Render a frame.  Return False if closed.  Useful for unit test.'
    ogre.WindowEventUtilities().messagePump()
    return ogre_root.renderOneFrame()


# For applications that do not have logListener attribute.
logListener = None
logManager = None

class quiet_logListener_class(ogre.LogListener):
    def messageLogged(self, message, level, debug, logName):
        '''Called by Ogre instead of logging.'''
        pass
        #print message


def quiet_log():
    '''Replace log with quiet version.  Useful for unit test.  
    Return logManager and logListener, which must destructed AFTER root.  
    >>> logManager, logListener = quiet_log()
    
    >>> root, sceneManager, renderWindow, camera = setup_unittest()

    Gotcha:  If you encounter 'R6025 Pure virtual function call' error within a class, then write destructor to destroy root before logManager and logListener.  http://www.indiegamer.com/archives/t-3533.html
    >>> del root
    >>> del sceneManager, renderWindow, camera
    >>> del logManager, logListener

    Derived from examples:
    http://www.ogre3d.org/phpBB2addons/viewtopic.php?p=10887&sid=ce193664e1d3d7c4af509e6f4e2718c6
    http://wiki.python-ogre.org/index.php/ChangeLog
    '''
    logManager = ogre.LogManager()
    log = ogre.LogManager.getSingletonPtr().createLog(
            'quiet.log', True, False, True)
    logListener = quiet_logListener_class()
    log.addListener(logListener)
    return logManager, logListener


class application_class(object):
    '''Minimal Ogre application, which needs reference to root.
    >>> application = setup_quiet_application(setup_unittest)
    >>> for i in range(10):
    ...     print i,
    ...     if not renderOneFrame(application.root):  print False
    0 1 2 3 4 5 6 7 8 9
    >>> assert application
    '''
    def __init__(self):
        self.root = None
        self.sceneManager = None
        self.renderWindow = None
        self.camera = None
        # For quiet_log
        self.logManager = None
        self.logListener = None

    def __del__(self):
        del self.sceneManager
        del self.root
        del self.renderWindow
        del self.camera
        # Must delete root before logManager and logListener
        del self.logListener
        del self.logManager


def setup_quiet_application(setup_function = setup, application = None):
    '''Return a minimal, application with logging disabled. 
    >>> application = setup_quiet_application(setup_unittest)

    Alternatively try to make an application be quiet.
    >>> application = application_class()
    >>> application = setup_quiet_application(setup_unittest, application)
    '''
    if not application:
        application = application_class()
    if hasattr(application, 'logManager') \
            and hasattr(application, 'logListener'):
        if quiet_logListener_class != type(application.logListener):
            application.logManager, application.logListener = quiet_log()
    else:
        global logListener, logManager
        logManager, logListener = quiet_log()
    application.root, application.sceneManager, application.renderWindow, application.camera = setup_function()
    return application


def setup_unittest_application(application = None):
    '''Convenience function to avoid accessing namespace.
    >>> application = setup_unittest_application()
    >>> del application

    Try to setup an existing application quietly.
    >>> application = application_class()
    >>> application = setup_unittest_application(application)
    '''
    return setup_quiet_application(setup_unittest, application)


def setup_unittest_sample_framework_application(application):
    '''Setup a unit test for SampleFramework, by assigning camera and renderWindow.
    >>> import ogre.renderer.OGRE.sf_OIS as sf
    >>> application = sf.Application()
    
    >>> application = setup_unittest_sample_framework_application(application)
    >>> application.sceneManager.clearScene()
    >>> del application
    '''
    application = setup_quiet_application(setup_unittest, application)
    if hasattr(application, 'camera') and not application.camera:
        if application.sceneManager.hasCamera('Camera'):
            application.camera = application.sceneManager.getCamera('Camera')
        elif hasattr(application, '_createCamera'):
                application._createCamera()
    if hasattr(application, '_createViewports'):
        #print '--- createScene'
        application._createViewports()
    if hasattr(application, '_createScene'):
        #print '--- createScene'
        application._createScene()
    if hasattr(application, 'frameListener'):
        if hasattr(application, '_createFrameListener'):
            #print '--- createFrameListener'
            application._createFrameListener()
    return application


def go(application):
    '''Convenience for an application.'''
    if hasattr(application, 'go'):
        application.go()
    else:
        run(application.root, application.sceneManager, application.renderWindow, application.camera)
 

if __name__ == '__main__':
    import code_util
    code_util.test(__file__)
