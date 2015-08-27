from config import Config
import datetime
import logging


class AppLog:
    
    config=None 
    logfilename=None
    
    def __init__(self):
        conf=Config()
        self.config =conf.getConfParser()
        self.logfilename=self.config.get('files','log')
    
    def logInfo(self,text):
        logging.basicConfig(filename=self.logfilename,level=logging.DEBUG)
        logging.info(str(datetime.datetime.now())+' : '+text)
