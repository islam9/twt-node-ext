from config import *
import MySQLdb

class MySQLHelper:  
    
    server=''
    username=''
    password=''
    dbname=''    
    config=None 
    dbconn=None

    def __init__(self,_server='',_username='',_password='',_dbname=''):
        if _server is '': 
            conf=Config()
            self.config =conf.getConfParser()           
            self.server = self.config.get('databases','server')
            self.dbname = self.config.get('databases','dbname')
            self.username = self.config.get('databases','username')
            self.password = self.config.get('databases','password')
        else:
            self.server = _server
            self.dbname = _dbname
            self.username = _username
            self.password = _password
        
    def opendb(self):
        try:
            self.dbconn= MySQLdb.connect (self.server,self.username, self.password,self.dbname,charset='utf8') 
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            exit (1)
    
    def closedb(self):
        try: 
            self.dbconn.commit ()
            self.dbconn.close()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            exit (1)
            
    def query(self,_query):
        try: 
            self.opendb()
            cursor = self.dbconn.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(_query)
            result=cursor.fetchall()
            cursor.close ()
            self.closedb()
            return result
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            exit (1)
  
    def multiquery(self,_query):
        ResultArray=[]
        try: 
            self.opendb() 
            cursor = self.dbconn.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(_query) 
            ResultArray.append(cursor.fetchall())
            while cursor.nextset():
                ResultArray.append(cursor.fetchall())
            self.closedb()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return ResultArray
             
    def querydynamic(self,_query,_array):
        try: 
            self.opendb()
            cursor = self.dbconn.cursor()           
            cursor.executemany(_query,_array)
            cursor.close ()
            self.closedb()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            exit (1)
            
    def executequery(self,_query,_tuble):
        try: 
            self.opendb()
            cursor = self.dbconn.cursor()           
            cursor.execute(_query,_tuble)
            cursor.close ()
            self.closedb()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            exit (1)
