from pygame import image,Surface,draw
import glob
import os
import configparser

def isInt(n):
    if n[0] == "-" and len(n) > 1 and n[1:].isnumeric():
        return True
    elif n.isnumeric():
        return True
    return False

def isFloat(n):
    return isInt(n.replace(".","",1))


class DataBlock():
    def __init__(self,Type):
        self.Type = Type # what type of data is this block?
        
    def __setitem__(self,key,value):
        if isinstance(value,str):
            if isInt(value):
                value = int(value)
            elif isFloat(value):
                value = float(value)
        
        self.__setattr__(key,value)
    
class AssetManager():
    '''
    Manages Assets
    '''
    cp = None
    assets = {}
    imageSets = {}
    spriteData = {}
    
    @classmethod
    def init(cls,configFileName):
        cls.cp = configparser.ConfigParser()
        cls.cp.optionxform = str
        cls.loadAssets(configFileName)
        cls.loadSpriteData()
        
    @classmethod
    def loadAssets(cls, configFileName):
        '''
        Loads assets based on the contents of the config file; should be in INI
        format.
        '''
        
        cls.cp.read_file(open(configFileName,"r"))
        #load images
        for each in cls.cp["images"].items():
           cls.assets[each[0]] = image.load("Assets/"+each[1])
           cls.assets[each[0]].convert()

        cls.cp["images"].clear()
        
    @classmethod
    def getAsset(cls, key):
        '''
        Returns a pygame.Surface, a sound or maybe something else in the future
        Raises a RuntimeError (maybe something else in the future) if assets
        haven't been loaded yet.
        '''
        if cls.cp == None:
            raise RuntimeError("AssetManager hasn't loaded assets yet!")
        try:
            return cls.assets[key]
        except: # you sure you don't want an exception?
            print ("An Error occured while trying to retrieve key \""+key+"\"!")

    @classmethod
    def loadSpriteData(cls):
        '''
        Loads the skeletal information (e.g. number of frames) for sprites from /Assets/Sprite/.
        Doesn't load the images yet.
        Raises a RuntimeError if an .ini file is missing the needed [sprite] section.
        '''
        sets = os.listdir("Assets/Sprite/")
        if ".svn" in sets:
            sets.remove(".svn")
        for each in sets:
            sprites = os.listdir("Assets/Sprite/%s/"%each)
            if ".svn" in sprites:
                sprites.remove(".svn")
            setData = {}
            for sprite in sprites:
                cls.cp.read_file(open("Assets/Sprite/%s/%s/data.ini"%(each,sprite),"r"))
                try:
                    item = cls.cp["sprite"]
                except:
                    raise RuntimeError("Data for {} doesn't have sprite section!".format(sprite))

                data = DataBlock("sprite")
                imageSet = []

                n = int(item.pop("numImages"))
                
                for x in item.items():
                    data[x[0]] = x[1]

                for i in range(n):
                    img = image.load("Assets/Sprite/%s/%s/%04i.png"%(each,sprite,i+1))
                    img = cls.reCenterImage(img,data.offX,data.offY)
                    imageSet.append(img)
                    
                data["imageSet"] = imageSet

                setData[sprite] = data
                cls.cp["sprite"].clear()
            cls.spriteData[each] = setData

    @classmethod
    def reCenterImage(cls,img,offx,offy):
        buffer = img.copy()
        w,h = img.get_width(),img.get_height()
        draw.rect(buffer,(0,0,0,0),(0,0,w,h))
        buffer.blit(img,(w/2-offx,h/2-offy))
        return buffer
            
    @classmethod        
    def getSpriteData(cls,key):
        if key in cls.spriteData:
            return cls.spriteData[key]
        raise KeyError("Key '{}' not in Sprite Data!".format(key)) 
