import urllib
import urllib2
import cookielib
import re
import threading
import json
import Queue
import logging

class BattleQuery(threading.Thread):
    
    def setup(self):
        self.queryQueue=Queue.Queue()
        self.cJar=cookielib.CookieJar()
        self.blOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cJar))
        logging.info("done setting up battlequery")
    
    def authenticate(self, email, password):
        self.blOpener.open("http://battlelog.battlefield.com/bf3/gate/login",  urllib.urlencode({"email": email, "password": password, "submit": "Sign in"}) )
    
    def resolveName(self, username):
        ##returns soldier id
        try:
            page=self.blOpener.open("http://battlelog.battlefield.com/bf3/user/"+urllib.quote(str(username))+"/").read()
        except urllib2.HTTPError:
            return False
        else:
            p=re.compile("/bf3/soldier/"+username+"/stats/([0-9]*)/", re.IGNORECASE)
            match=p.search(page)
            try:
                uid = match.group(1)
            except AttributeError:
                return False
            else:
                return uid
        
    def queryBasicStats(self, uid):
        return json.loads(self.blOpener.open("http://battlelog.battlefield.com/bf3/overviewPopulateStats/"+urllib.quote(str(uid))+"/bf3-ru-assault/1/").read())["data"]["overviewStats"]
        
    def resolveQueryAndCallback(self, username, modInstance, funcName):
        try:
            call=getattr(modInstance, funcName)
        except AttributeError:
            return False
        else:
            self.queryQueue.put((username, call))
            return True
    
    def run(self):
        while True:
            item=self.queryQueue.get()
            item[1](item[0], self.queryBasicStats( self.resolveName(item[0])))

#class dummymod():
#    def callback(self, jsondata):
#        print jsondata["deaths"]
#
#d=dummymod()
#
#bQ=battleQuery()
#bQ.setupQueue()
#bQ.authenticate("username", "password")
#uid=bQ.resolveName("abc")
#bQs=bQ.queryBasicStats(uid)
#bQ.start()
#bQ.resolveQueryAndCallback("username", d, "callback")
#