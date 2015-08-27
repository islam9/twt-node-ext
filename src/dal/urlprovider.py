from helper.applog import AppLog
from helper.mysqlhelper import MySQLHelper

class Urlprovider:
    
    logger=None
    
    def __init__(self):
        self.logger=AppLog()
 
    def getPosts(self):
        try:
            dbObj=MySQLHelper()
            query="select * from posts where urlextracted=0 order by id;"
            result=dbObj.query(query)
            return result
        except:
            self.logger.logInfo('Exception in getPosts method (dal/urlprovider.py)')
            
    def addURL(self,url,orgurl,postid):
        try:
            dbObj=MySQLHelper()
            query="select id,counter from urls where orgurl='"+orgurl+"'"
            result=dbObj.query(query)
            if len(result) == 0:
                tubleData=(url,orgurl,postid)
                query="insert into urls (url,orgurl,postid) values (%s,%s,%s)"
                result=dbObj.executequery(query,tubleData)
            else:
                query=''
                id=result[0]['id']
                counter=result[0]['counter']
                if counter is None:
                    counter=0
                counter += 1
                query="update urls set counter="+str(counter)+" where id="+str(id)
                result=dbObj.query(query)

        except:
            self.logger.logInfo('Exception in addURL method (dal/urlprovider.py)')
            
    def updatePostUrlExtracted(self,postid,value):
        try:
            dbObj=MySQLHelper()
            query="update posts set urlextracted="+str(value)+" where id="+str(postid)
            result=dbObj.query(query)
            return result
        except:
            self.logger.logInfo('Exception in updatePostStatus method (dal/twitterprovider.py)')
            
    def getURLs(self):
        try:
            dbObj=MySQLHelper()
            query="select * from urls where status=0"
            result=dbObj.query(query)
            return result
        except:
            self.logger.logInfo('Exception in updatePostStatus method (dal/twitterprovider.py)')
            
    def addUrlHeaderInfo(self,urlid,metatitle,metadescription):
        try:
            dbObj=MySQLHelper()
            tubleData=(metatitle,metadescription)
            query="update urls set metatitle=%s,metadescription=%s where id="+str(urlid)
            result=dbObj.executequery(query,tubleData)
            return result
        except:
            self.logger.logInfo('Exception in updatePostStatus method (dal/twitterprovider.py)')
            
    def saveUrlIMG(self,urlid,filename):
        try:
            dbObj=MySQLHelper()
            tubleData=(urlid,filename)
            query="insert into urlimgs (urlid,filename) values (%s,%s)"
            result=dbObj.executequery(query,tubleData)
            return result
        except:
            self.logger.logInfo('Exception in saveUrlIMG method (dal/twitterprovider.py)')
            
    def updateUrlStatus(self,urlid,value):
        try:
            dbObj=MySQLHelper()
            query="update urls set status="+str(value)+" where id="+str(urlid)
            result=dbObj.query(query)
            return result
        except:
            self.logger.logInfo('Exception in updateUrlStatus method (dal/twitterprovider.py)')
            