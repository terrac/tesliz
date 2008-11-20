from tesliz.runthis import *
import data.maps.scene02


def startup():
    a =data.maps.scene02.Unitdata()
    a.setuptestmap()
    s.app.loadScene("scene02")
    pass

if __name__ == '__main__':
#    try:
    application = OgreNewtonApplication(startup)
    application.go()