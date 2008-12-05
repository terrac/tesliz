import tesliz.runthis
from tactics.Singleton import *
import sys


def startup():
    s.framelistener.pauseturns = False
    s.app.loadScene(sys.argv[1],True)
    pass

if __name__ == '__main__':
#    try:
    application = tesliz.runthis.OgreNewtonApplication(startup)
    application.go()