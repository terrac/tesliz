from tesliz.runthis import *



def startup():
    s.app.loadScene("scene01")
    pass

if __name__ == '__main__':
#    try:
    application = OgreNewtonApplication(startup)
    application.go()