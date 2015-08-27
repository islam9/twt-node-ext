#encoding:UTF-8
from PIL import Image
from config import Config
from dal.urlprovider import Urlprovider
from helper.applog import AppLog
from helper.beautifulsoup import BeautifulSoup
from helper.httpexists import httpExists
from helper.urlhelper import UrlHelper
from urllib import urlretrieve
import os
import sys
import urllib2
import urlparse
import uuid

def getUrlHTMLsoup(url):
    try:
        html = urllib2.urlopen(url)
        soup = BeautifulSoup(html)
        return soup
    except:
        return None

def retriveImg(url,outpath):
    urlretrieve(url,outpath)
    
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]


    
def getUrlImgs(url,urlid,soup):
    
    config=Config()
    myConfiguration=config.getConfParser()
    out_folder=myConfiguration.get('files', 'img')
    
    imagelist=[]
    urlHelpObj=UrlHelper()
    parsed = list(urlparse.urlparse(url))
    pathParsed=parsed[2]  

    for image in soup.findAll("img"):
        try:  
            src= image['src']
            if src:
                filename = image["src"].split("/")[-1]
                outpath = os.path.join(out_folder, filename)
                extension = os.path.splitext(outpath)[1]
                
                if extension.lower() in ['.gif','.jpg','.png','.bmp','.jpeg','.tif','.tiff']:
                    if urlHelpObj.isUrl(src):
                        retriveImg(src,outpath)
                        imagelist.append(filename)
                    else:
                        parsed[2] = image["src"]
                        urlExist=httpExists(urlparse.urlunparse(parsed))
                        if urlExist==1:
                            retriveImg(urlparse.urlunparse(parsed),outpath)
                            imagelist.append(filename)
                        else:
                            virDirs=pathParsed.split('/')
                            for dir in virDirs:
                                if dir:
                                    parsed[2] = dir+"/"+image["src"]
                                    urlExist=httpExists(urlparse.urlunparse(parsed))
                                    if urlExist==1:
                                        retriveImg(urlparse.urlunparse(parsed),outpath)
                                        imagelist.append(filename)
        except:
            logger.logInfo("no src found in img tag  : "+str(sys.exc_info()[0]))
            
    imagelist=f7(imagelist)
    imageProcessing(urlid,imagelist)
    
def imageProcessing(urlid,imgList):
    config=Config()
    myConfiguration=config.getConfParser()
    out_folder=myConfiguration.get('files', 'img')
    
    urlproviderObj=Urlprovider()
    saveImgList=[]
    
    for img in imgList:
        try:
            newSize=(450,300)
            imgfile=out_folder+"/"+img
            im = Image.open(imgfile)
            imgwidth= im.size[0]
            imgheight= im.size[1]
            imgformat=im.format
            
            if imgwidth < 75 or imgheight < 50:
                os.remove(imgfile)
            else:
                extension=os.path.splitext(img)[1]
                newImgName=str(uuid.uuid1())+str(extension)
                im.thumbnail(newSize, Image.ANTIALIAS)
                im.save(out_folder+"/"+newImgName,imgformat)
                os.remove(imgfile)
                saveImgList.append(newImgName)
        except:
            logger.logInfo("in urldatagrapper.py open images  : "+str(sys.exc_info()[0]))
                
    for saveimg in saveImgList:
        urlproviderObj.saveUrlIMG(urlid,saveimg)
        


                            
logger=AppLog()
urlproviderObj=Urlprovider()
urlHelpObj=UrlHelper()

try:

    urls=urlproviderObj.getURLs()

    for url in urls:
        if httpExists(url['orgurl']):
            urlid=url['id']
            soup=getUrlHTMLsoup(url['orgurl'])
            if soup:
                headrDict=urlHelpObj.getHeaderInfo(soup)
                urlproviderObj.addUrlHeaderInfo(urlid,headrDict['title'], headrDict['description'])
                getUrlImgs(url['orgurl'],urlid,soup)
                urlproviderObj.updateUrlStatus(urlid,1)
            else:
                urlproviderObj.updateUrlStatus(urlid,2)
        else:
            urlproviderObj.updateUrlStatus(urlid,3)
                
except:
    logger.logInfo("in urldatagrapper.py  : "+str(sys.exc_info()[0]))
