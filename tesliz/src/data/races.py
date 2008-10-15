from tactics.race import *
import ogre.renderer.OGRE as Ogre

class Races:
    def __init__(self):
        self.map = map = dict()
        map["Human"] = Race()
        map["Kobold"] = Race(Ogre.Vector3(.5,.5,.5))
    