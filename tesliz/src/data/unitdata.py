from tactics.util import *

class Unitdata(object):
    def axis2(self,unit):
        buildUnit(unit,"FastFighter","Player1")
        buildPhysics(unit)
                       
    def axis(self,unit):
        buildUnit(unit,"SlowFighter","Computer1")
        buildPhysics(unit)