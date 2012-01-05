import threading
import time
import uuid

class Announcer(threading.Thread):
    def __init__(self, actionHandler):
        self.messageQueue=[]
        self.actionHandler=actionHandler
        self.currentMessageIndex=0
        self.pause=False
        threading.Thread.__init__(self)
    
    def addMessages(self, messagesString):
        return map(self.addMessage, messagesString.split("|"))
    
    def addMessage(self, message):
        mId=uuid.uuid4()
        if message[0:2]=="&w" and message[2:].isdigit():
            self.messageQueue.append( (mId, int(message[2:])) )
        else:
            self.messageQueue.append( (mId, str(message)) )
        return mId
        
    def removeMessages(self, messageIds):
        for mId in messageIds:
            for i,v in enumerate(self.messageQueue):
                if v[0]==mId:
                    self.messageQueue.pop(i)
                    break

    def run(self):
        while True:
            if not self.pause and len(self.messageQueue)>0:
                if self.currentMessageIndex > len(self.messageQueue)-1:
                    self.currentMessageIndex=0
                    time.sleep(10) 
                
                try:
                    currentMessage=self.messageQueue[self.currentMessageIndex][1]
                except IndexError:
                    pass
                else:
                    if isinstance(currentMessage, int):
                        time.sleep(int(currentMessage))
                    else:
                        self.actionHandler.sayAll(str(currentMessage))
                    
                    self.currentMessageIndex+=1
            else:
                time.sleep(5)
                
#s=announcer(0)
#s.start()
#msg=s.addMessages("&w123|&w222")
#msg2=s.addMessages("&w1337")
#s.removeMessages(msg)
