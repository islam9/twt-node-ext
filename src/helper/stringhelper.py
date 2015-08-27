import  re


class stringHelper:  
    
    URL_Regex='http?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    
    def extractURL(self,text):
        
        URLsList=[]
        URLS= re.findall(self.URL_Regex,text)
        
        for url in URLS:
            while url[-1]=='.':
                url = url[:-1]
            URLsList.append(url) 
                
        return URLsList

    def trimTweet(self,text):
        text = text.strip(' \t\n\r')
        text = text.strip()
        text = text.lstrip()
        text = text.rstrip()
        return text.lower()  

