from helper.applog import AppLog
import re
import socket
import urllib2
import sys

class UrlHelper:
    
    logger=None
    
    def __init__(self):
        self.logger=AppLog()
        
    def isUrl(self,url):
        p = re.compile('http?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        m= p.match(url)
        if m:
            return True
        else :
            return False
  
    def getRealURL(self,url):
        try:
            socket.setdefaulttimeout(30)
            realURL=urllib2.urlopen(url).geturl()
            return realURL
        except urllib2.HTTPError:
            self.logger.logInfo('Exception in getRealURL method urllib2.HTTPError (helper/urlhelper.py)'+str(sys.exc_info()[0]))
            return None
        except urllib2.URLError:
            self.logger.logInfo('Exception in getRealURL method  urllib2.URLError (helper/urlhelper.py)'+str(sys.exc_info()[0]))
            return None
        except:
            return None
        
    def getHeaderInfo(self,soup):
        headrDict = {}
        title=None
        meta=[]
        description=None
        metaTitle=None
        
        try:
            title = soup.find('head').title.string
            meta = soup.findAll('meta')
        except:
            self.logger.logInfo('getHeaderInfo some meta tags function not tags (helper/urlhelper.py) ')
        
        for m in meta:
            try:
                if m['name'].lower()=='title':
                    metaTitle=m['content']
                    if metaTitle:
                        title=metaTitle
                elif m['name'].lower()=='description':
                    description=m['content']
            except:
                self.logger.logInfo('getHeaderInfo some meta tags function not tags (helper/urlhelper.py)')
    
        headrDict['title']=title
        headrDict['description']=description
        return headrDict