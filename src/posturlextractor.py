#encoding:UTF-8
from dal.urlprovider import Urlprovider
from helper.applog import AppLog
from helper.stringhelper import stringHelper
from helper.urlhelper import UrlHelper
import sys

logger=AppLog()
strObj=stringHelper()
ulrObj=UrlHelper()
urlpObj=Urlprovider()

try:
    
    posts=urlpObj.getPosts()
    
    for post in posts:
        
        postid=post['id']
        postText=post['text']
        postURLs=strObj.extractURL(postText)
        
        for url in postURLs:
            if url:
                orgurl=ulrObj.getRealURL(url)
                if orgurl:
                    urlpObj.addURL(url, orgurl, postid)
                    
        urlpObj.updatePostUrlExtracted(postid,1)
        
except:
    logger.logInfo("in post url extractor  : "+str(sys.exc_info()[0]))
                
    

