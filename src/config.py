import ConfigParser

config = ConfigParser.ConfigParser()
config.read("config/config.cfg")  

class Config:  
    
    config=None 
    
    def islam(self):
        print('isa') 
    
    def __init__(self): 
        config = ConfigParser.ConfigParser()
        config.read("config/config.cfg")  
        
        
    def getConfParser(self):
        return  config  
         
