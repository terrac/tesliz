import random
import copy
import shelve
class Enum:

    """Create an enumerated type, then add var/value pairs to it.
    The constructor and the method .ints(names) take a list of variable names,
    and assign them consecutive integers as values.    The method .strs(names)
    assigns each variable name to itself (that is variable 'v' has value 'v').
    The method .vals(a=99, b=200) allows you to assign any value to variables.
    A 'list of variable names' can also be a string, which will be .split().
    The method .end() returns one more than the maximum int value.
    Example: opcodes = Enum("add sub load store").vals(illegal=255)."""
  
    def __init__(self, names=[]): 
        #self.ints(names) 
        self.strs(names)

    def set(self, var, val):
        """Set var to the value val in the enum."""
        if var in vars(self).keys(): raise AttributeError("duplicate var in enum")
        if val in vars(self).values(): raise ValueError("duplicate value in enum")
        vars(self)[var] = val
        return self
  
    def strs(self, names):
        """Set each of the names to itself (as a string) in the enum."""
        self.enumlist = self._parse(names)
        for var in self.enumlist: self.set(var, var)
        return self

    def ints(self, names):
        """Set each of the names to the next highest int in the enum."""
        self.enumlist = self._parse(names)
        for var in self.enumlist: self.set(var, self.end())
        return self
    def __iter__(self):
        return self.enumlist.__iter__()

    def vals(self, **entries):
        """Set each of var=val pairs in the enum."""
        for (var, val) in entries.items(): self.set(var, val)
        return self

    def end(self):
        """One more than the largest int value in the enum, or 0 if none."""
        try: return max([x for x in vars(self).values() if type(x)==type(0)]) + 1
        except ValueError: return 0
    
    def _parse(self, names):
        ### If names is a string, parse it as a list of names.
        if type(names) == type(""): return names.split()
        else: return names
class Pair:
    def __init__(self,key,value = None):
        
        if not hasattr(key, "__iter__"):
            key =[key]            
        if not isinstance(value, list):
            value = [value]
        self.key = key
        self.value = value
    def __str__(self):
        x = ""
        for y in self.value:
            x = x+","+str(y)
        return str(self.key)+", "+str(x)
    def getKey(self):
        return self.key[0]


class Area:
    size = 5
    generated = None
    variables = None
    templatelist = None
    objects = None
    def getVariables(self):
        if not self.objects:
            return False
        return [self.objects]
    def execute(self,area):
        vars =self.pickvars(area)
        
        self.generate(vars)
        if area.generated:
            area.generated = area.generated + self.generated
        else:
            area.generated = self.generated 
    def type(self):
        return self.__class__.__name__
    def pickvars(self,area):
        #pick similar vars to what has been previously passed in
        vars = self.getVariables()
        vals = []
        for x in range(0,self.size):
            val = vars[len(vars)-1]
            vals.append(val)
                    
        if area.generated == None:
            return vals
        else:
            return area.generated + vals
        

    def generate(self,vals):
        self.generated = []
        
        for x in vals:
            y = self.getRandomValid(x)
            
            if y:
                #tem = y.getClosest(y,self.templatelist)
#                if not self.templatelist:
#                    self.generated.append(Pair(None,y))    
#                    continue
                for x in self.templatelist:
                    if y == x.getKey():
                       x.type = self.type()
                       self.generated.append(copy.deepcopy(x))
                       break
                      
    def getRandomValid(self,x):
    #iterate through variables in an orderly fashion and then iterate through x and return the first valid match
    #on the variables it will iterate through the varibles and produce any items in an enum or whatever
        valid = []
        for y in self.getVariables():
            if isinstance(x, Pair):
                valid.append(x.getKey())
                continue
            for a in x:
                if not hasattr(y,"__iter__"):
                    if a == y:
                        valid.append( a)
                    continue
                for z in y:
                    if a == z:
                        valid.append(a)
                        #random.randrange(0,5)
        return valid[random.randrange(0,len(valid))]
    

    
#import tactics.TerrainManager    
#class Map(Area):
#    def execute(self,area):
#        area.terrainmanager = tactics.TerrainManager.TerrainManager()
        
class Positions(Area):
    where = Enum("high low like")
    x = 10
    y = 10
    z = 10
    def getVariables(self):
        self.variables = []
        for x in range(0,self.size):
            self.variables.append((random.randint(0,self.x),random.randint(0,self.x),random.randint(0,self.x)))
        return self.variables
        #randomly get some numbers and assign them
    def getRandomValid(self,x):
        return self.variables[random.randint(0,len(self.variables))-1]
    def __init__(self):
        #like just says that positions should be assigned to like units
        #so a high unit gets a high position
        #the generator would have to do the actual stuff
        

        self.templatelist = None
    def pickvars(self,area):
        self.getVariables()
        return area.generated 
    def generate(self,vals):
        self.generated = []
        
        for x in vals:
            y = self.getRandomValid(x)            
            #self.generated.append(Pair(None,y))
            x.value.append(Pair("Position",y))    

class Players(Area):
    objects = Enum("Player1 Computer1")
 
    def getRandomValid(self,x):
        li = self.objects.enumlist
        return li[random.randint(0,len(li)-1)]
    def generate(self,vals):
        self.generated = []
        
        for x in vals:
            y = self.getRandomValid(x)            
            #self.generated.append(Pair(None,y))
            if hasattr(x, "value"):
                x.value.append(Pair("Playername",y))
class Characters(Area):
    objects =Enum("fighter mage")

    def __init__(self):
        
        self.templatelist =[Pair(self.objects.fighter),Pair(self.objects.mage)]
    
    
class Landmarks(Area):
    objects =Enum("mountain lake plain river")

    def __init__(self):
        
        self.templatelist =[Pair(self.objects.mountain,(0,0,0)),Pair(self.objects.river,(2,0,2)),Pair(self.objects.plain,(2,0,2)),Pair(self.objects.lake,(2,0,2))]
    

area = Area()
char = Characters()
char.execute(area)

players = Players()
players.execute(area)
land = Landmarks()
land.execute(area)
pos = Positions()
pos.execute(area)

#      in area.generated:
#   print x
map = shelve.open("test.map")
for x in area.generated:
    
    print x
map.close()
#Characters.execute(self, area)    
#Positions.execute(self, area)