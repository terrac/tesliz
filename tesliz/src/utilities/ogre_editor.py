#!/usr/bin/python

'''Proof of concept for a lightweight PythonCard user interface to monitor and edit Python-Ogre properties.  Ogre application is decoupled from editor.
'''
__author__ = 'Ethan Kennerly'
__date__ = '2008-01-31'

from PythonCard import model, configuration
import code_util
import ogre_util
import ogre_unit

color = None
import_file = None


def dialog_getOgreColourValue( ogre ):
    result = dialog.colorDialog()
    if result.accepted:
        # Convert PythonCard [0-255] color value to ogre [0.0-1.0] color.
        r = float(result.color[0])/255.0
        g = float(result.color[1])/255.0
        b = float(result.color[2])/255.0
        return ogre.ColourValue( r,g,b )
    return None


def try_float(value):
    try:
        value = float(value)
    except:
        return None
    return value


class ogre_background_class(model.Background):
    '''PythonCard user interface for rbert prototype.
    >>> application = model.Application( ogre_background_class )
    >>> background = application.backgrounds[0]
    '''
    def on_initialize(self, event):
        self.node = None
        self.app = None
        # TODO:  class data member instead of global?
        global import_file
        if import_file:
            self.import_ogre_app( import_file, locals(), globals() )
    def on_activate(self, event):
        if self.app:
            self.app.renderWindow.setActive(True)
    def import_ogre_app( self, file, locals, globals ):
        '''Launch ogre app from file and attach app.'''
        # Often times, I want to script in the shell in the same namespace.
        code_util.import_file( file, locals, globals, 
                this_namespace = True )
        global ogre
        assert ogre
        application_class = eval(self.components.ogre_application_class.text)
        self.app = application_class()
        ogre_unit.go(self.app)
    def on_import_mouseClick(self, event):
        result = dialog.fileDialog()
        if result.accepted:
            file = result.paths[0]
            self.import_ogre_app(file, locals(), globals())
    def on_startRendering_mouseClick(self, event):
        self.app.root.startRendering()
    def on_setAmbientLight_mouseClick(self, event):
        global ogre
        self.app.sceneManager.setAmbientLight( dialog_getOgreColourValue( ogre ) )
    def on_color_mouseClick(self, event):
        dialog_color = dialog_getOgreColourValue( ogre )
        if dialog_color:
            global color
            color = dialog_color
            if self.components.colorFunction.text: 
                color_function = eval( self.components.colorFunction.text )
                color_function( color )
    def on_sceneNodeRefresh_mouseClick(self, event):
        if self.app:
            root_node = self.app.sceneManager.getRootSceneNode()
            self.components.sceneNode.items = ogre_util.sorted_child_name_list( 
                    root_node )
    def on_sceneNode_select(self, event):
        if self.app:
            name = self.components.sceneNode.items[
                    self.components.sceneNode.selection ]
            if self.app.sceneManager.hasSceneNode( name ):
                if self.node:
                    if self.node.getShowBoundingBox():
                        self.node.showBoundingBox( False )
                self.node = self.app.sceneManager.getSceneNode( name )
                self.node.showBoundingBox( True )
                self.observe_position(self.node)
                self.observe_rotation(self.node)
            else:
                print 'sceneNode not in sceneManager:', name, \
                    str(self.app.sceneManager)

    def observe_position(self, node):
        if node:
            self.components.x.text = str(node.position.x)
            self.components.y.text = str(node.position.y)
            self.components.z.text = str(node.position.z)
    def on_x_loseFocus(self, event):
        if self.node:
            self.node.position = ogre_util.x(self.node.position, try_float(self.components.x.text))
            self.observe_position(self.node)
    def on_y_loseFocus(self, event):
        if self.node:
            self.node.position = ogre_util.y(self.node.position, try_float(self.components.y.text))
            self.observe_position(self.node)
    def on_z_loseFocus(self, event):
        if self.node:
            self.node.position = ogre_util.z(self.node.position, try_float(self.components.z.text))
            self.observe_position(self.node)

    def observe_rotation(self, node):
        if node:
            self.components.pitch.text = str(
                    node.orientation.getPitch().valueDegrees())
            self.components.yaw.text = str(
                    node.orientation.getYaw().valueDegrees())
            self.components.roll.text = str(
                    node.orientation.getRoll().valueDegrees())
    def on_yaw_loseFocus(self, event):
        ogre_util.set_yaw(self.node, try_float(self.components.yaw.text))
        self.observe_rotation(self.node)
    def on_pitch_loseFocus(self, event):
        ogre_util.set_pitch(self.node, try_float(self.components.pitch.text))
        self.observe_rotation(self.node)
    def on_roll_loseFocus(self, event):
        ogre_util.set_roll(self.node, try_float(self.components.roll.text))
        self.observe_rotation(self.node)


def main():
    configuration.setOption('showShell', True)
    configuration.setOption('showDebug', True)
    # Precondition:  Configuration options in configuration.configDict set.
    pythoncard_app = model.Application(ogre_background_class)
    pythoncard_app.MainLoop()
    background = pythoncard_app.backgrounds[0]


if __name__ == '__main__':
    # Default behavior when executed directly
    import sys
    # PythonCard built-in options
    #     -d:  debug
    #     -s:  shell
    import_arg = False
    for arg in sys.argv:
        if arg == '--test':
            code_util.test(__file__)
            break
        elif arg == '--import':
            import_arg = True
        elif import_arg:
            global import_file
            import_file = arg
    else:
        main()
