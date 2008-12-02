import ogre.gui.CEGUI as CEGUI
from utilities.CEGUI_framework import *
class OverviewTrade(object):
    def __init__(self):
        self.map = dict()
        
        self.pricemap = dict()
        #defaults
        self.pricemap["Cloth"] = 200
        self.pricemap["Leather"] = 500
        self.pricemap["Grain"] = 500
        self.pricemap["Wolf Pelt"] = 350
        self.addItem("Linder","Cloth",500)
        self.addItem("Linder","Leather",400)
        self.addItem("Exalia","Wolf Pelt",300)
        self.cmoney = 0
        self.items = ["Grain"]
        
        self.ilist = None
        
    #arrr 
    listholder = []    
        
    def addItem(self,place,item,money):
        if not self.map.has_key(place):
            self.map[place] = dict()
        self.map[place][item] = money
    
    def showItems(self,x,y,name):
        sheet = CEGUI.WindowManager.getSingleton().getWindow(  "root_wnd" )
        winMgr = CEGUI.WindowManager.getSingleton()
         
        if winMgr.isWindowPresent(name):            
            trade = winMgr.getWindow(name)
            trade.resetList()
        else:
            trade = winMgr.createWindow("TaharezLook/Listbox", name)
        sheet.addChildWindow(trade)
        trade.setText("actionlist")
        trade.setPosition(CEGUI.UVector2(cegui_reldim(x), cegui_reldim( y)))
        trade.setSize(CEGUI.UVector2(cegui_reldim(0.2), cegui_reldim( 0.2)))                
        #trade.setAlwaysOnTop(True)
        trade.subscribeEvent(CEGUI.Listbox.EventSelectionChanged, self, name)
        return trade
        
    
        
    def add(self,text,listbox ):        
        item =CEGUI.ListboxTextItem (text)        
        item.AutoDeleted = False     # Fix to ensure that items are not deleted by the CEGUI system 
        self.listholder.append(item)
        
        listbox.addItem(item)
    def show(self,placename):
        self.plist = self.showItems(.6, .5, "handleBuy")
        self.ilist = self.showItems(.8, .5, "handleSell")
        self.cplace = placename
        for x in self.items:
            self.add(x + "-"+str(self.getMoney(x)), self.ilist)
        for x in self.map[placename].keys():
            self.add(x + "-"+str(self.getMoney(x)), self.plist)
            
        sheet = CEGUI.WindowManager.getSingleton().getWindow(  "root_wnd" )
        winMgr = CEGUI.WindowManager.getSingleton()
        name = "money" 
        if winMgr.isWindowPresent(name):            
            trade = winMgr.getWindow(name)
        else:
            trade = winMgr.createWindow("TaharezLook/StaticText", name)
        sheet.addChildWindow(trade)
        trade.setText(str(self.cmoney))
        trade.setPosition(CEGUI.UVector2(cegui_reldim(.6), cegui_reldim( .4)))
        trade.setSize(CEGUI.UVector2(cegui_reldim(0.4), cegui_reldim( 0.1)))                
        #trade.setAlwaysOnTop(True)
        
        self.ceguimoney = trade
    def hide(self):
        winMgr = CEGUI.WindowManager.getSingleton()
        if self.ilist:
            winMgr.destroyWindow(self.ilist)
            winMgr.destroyWindow(self.plist)
            winMgr.destroyWindow(self.ceguimoney)
        
        
    def handleBuy(self,e):
        if not e.window.getFirstSelectedItem():
            return
        text = str(e.window.getFirstSelectedItem().getText())
        #item =e.window.getFirstSelectedItem()
        
        key = text.split("-")[0]
        money =self.getMoney(key)
        money = self.cmoney - money
        if self.setMoney(money):
            self.add(text, self.ilist)
            self.items.append(key)
        return True
        
    def handleSell(self,e):
        if not e.window.getFirstSelectedItem():
            return
        text = str(e.window.getFirstSelectedItem().getText())
        item =e.window.getFirstSelectedItem()
        
        key = text.split("-")[0]
        money = self.getMoney(key)
        money =self.cmoney + money

        self.setMoney(money)
        self.ilist.removeItem(item)
        self.items.remove(key)
        return True
    def getMoney(self,text):
        if self.map[self.cplace].has_key(text):
            return self.map[self.cplace][text]
        else:
            return self.pricemap[text]
    def setMoney(self,money):
        if money < 0:
            return False
        self.cmoney = money
        self.ceguimoney.setText(str(money))
        return True
    def save(self,map):
        map["items"] = self.items
        map["money"] = self.cmoney
    def load(self,map):
        self.items = map["items"]
        self.cmoney = map["money"]