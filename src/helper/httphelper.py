from helper.applog import AppLog
import httplib
import urlparse

class httpHelper:
    
    logger=None
    
    def __init__(self):
        self.logger=AppLog()
    
    def httpExists(self,url):
        
        host, path = urlparse.urlsplit(url)[1:3]
        found = None
        try:

            connection = httplib.HTTPConnection(host)  ## Make HTTPConnection Object
            connection.request("HEAD", path)
            responseOb = connection.getresponse()      ## Grab HTTPResponse Object
    
            if responseOb.status in [200,201,204,302]:
                found = responseOb.status

        except Exception, e:
            logvar= e.__class__,  e, url
            self.logger.logInfo(logvar)
            
        return found
    

