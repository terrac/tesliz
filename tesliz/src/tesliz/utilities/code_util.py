#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Utilities for importing and doctesting modules.
'''
__author__ = 'Ethan Kennerly'


def basefilename( path ):
    ''' Filename without the path or extension.
    >>> path = u'C:\\learnkorean\\source\\dance.py'
    >>> basefilename( path )
    u'dance'
    >>> basefilename( 'a.b.c.d.e' )
    'a.b.c.d'
    '''
    import os
    basename = os.path.basename( path )
    basefilename = os.path.splitext( basename )[0]
    return basefilename


def import_file( path, locals=locals(), globals=globals(), this_namespace=False ):
    '''Import module at the file in the absolute path.
    >>> import_file( 'C:\Python25\Lib\copy.py', locals(), globals() )
    <module 'copy' from 'C:\Python25\lib\copy.pyc'>
    >>> copy.name
    'CodeType'

    Import to this current namespace
    >>> import_file( 'C:\Python25\Lib\copy.py', locals(), globals(), True )
    '*'
    >>> type(deepcopy)
    <type 'function'>
    '''
    import os
    path = os.path.abspath(path)
    dirname = os.path.dirname(path)
    import sys
    if dirname not in sys.path:
        sys.path.append( dirname )
    os.chdir( dirname )
    module_name = basefilename(path)
    if not this_namespace:
        try:
            exec( 'import ' + module_name, locals, globals )
            return eval( module_name, locals, globals )
        except:
            print 'import failed', module_name, path
            exec( 'import ' + module_name, locals, globals )
    else:
        try:
            exec( 'from ' + module_name + ' import *', locals, globals )
            return '*'
        except:
            print 'from import failed', module_name, path
            exec( 'from ' + module_name + ' import *', locals, globals )


def test( path ):
    '''Test documented function examples in the module of the file path.
    #>>> test( __file__ )
    '''
    print
    import time
    print time.asctime(time.localtime(time.time()))
    print 'file', path
    module_name = basefilename( path )
    import doctest
    import_file( path )
    module = eval( module_name )

    print 'module', module_name, 'starts tests.'
    doctest.testmod( module )
    print 'module', module_name, 'finished tests.'


if __name__ == '__main__':
    test(__file__)
    #Pdb doesn't like __file__, so substitute file path.
    #test('code_util.py')

