def cleanup(key):

    if not key:
        return key
    
    if int(key.x) + .50 > key.x:
        key.x = int(key.x)
    else:
        key.x = int(key.x) + 1
    if int(key.y) + .50 > key.y:
        key.y = int(key.y)
    else:
        key.y = int(key.y) + 1
    if int(key.z) + .50 > key.z:
        key.z = int(key.z)
    else:
        key.z = int(key.z) + 1        

    return key


class VectorMap(dict):
    
   
    def __getitem__(self, key):
        key =cleanup(key)
        key = str(key)
        return dict.__getitem__(self,key)
        
    def __setitem__(self, key, value):
        key =cleanup(key)
        key = str(key)
        dict.__setitem__(self,key, value)
    
    def __delitem__(self, key):
              
        key = str(key)  
        dict.__delitem__(key)
    def has_key(self,key):
        key =cleanup(key)
        key = str(key)
        return dict.has_key(self,key)

