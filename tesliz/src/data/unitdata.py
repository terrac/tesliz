from tactics.util import *

class Unitdata(object):
    def axis2(self,unit):
        buildUnit(unit,"Fighter","Player1")
        buildPhysics(unit)
                       
    def axis(self,unit):
        buildUnit(unit,"Fighter","Computer1")
        buildPhysics(unit)